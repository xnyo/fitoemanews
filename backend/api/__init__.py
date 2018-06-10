import asyncio
import json
import traceback
from typing import Callable, Union

from aiohttp import web
from aiohttp.web_response import Response
from multidict import MultiDict
from schema import Schema, SchemaError, And, Use

from api import sessions
from constants.privileges import Privileges
from exceptions import api
from singletons.emanews import EmaNews


def readable_exception(exc: Exception, default: str) -> str:
    """
    Funzione che ritorna una stringa con il messaggio dell'eccezione `exc`
    o un messaggio di default, contenuto in `default`.

    :param exc: Eccezione
    :type exc: Exception
    :param default: Messaggio di default
    :type default: str
    :return: Messaggio dell'eccezione o messaggio di default
    :rtype: str
    """
    s = str(exc)
    return s if len(s) > 0 else default


def json_error_response(status: int, message: str) -> Response:
    """
    Metodo che ritorna una risposta aiohttp con un determinato
    status code e che contiene un oggetto JSON con due chiavi:
    status e message

    :param status: HTTP status code e stato che verrà inserito
    nell'oggetto JSON della risposta
    :type status: int
    :param message: Messaggio da inserire nell'oggetto JSON della
    risposta
    :type message: str
    :return: Risposta aiohttp
    :rtype: aiohttp.web_response.Response
    """
    return web.json_response(
        {
            "status": status,
            "message": message
        },
        status=status
    )


def multidict_to_dict(x: MultiDict) -> dict:
    """
    Funzione che converte un MultiDict in un dict

    :param x: MultiDict da convertire
    :type: MultiDict
    :return: dict corrispondente al MultiDict
    :rtype: dict
    """
    return {k: v if hasattr(v, "__len__") and len(v) <= 1 else x.getall(k) for k, v in x.items()}


def errors(f: Callable) -> Callable:
    """
    Decorator che gestisce gli errori dell'api

    :param f:
    :return:
    """
    async def wrapper(*args, **kwargs) -> Response:
        resp = web.json_response({}, status=200)
        try:
            resp = await f(*args, **kwargs)
        except api.NotFoundError as e:
            resp = json_error_response(404, readable_exception(e, "Resource not found"))
        except api.InternalServerError as e:
            resp = json_error_response(500, readable_exception(e, "Internal server error"))
        except api.ForbiddenError as e:
            resp = json_error_response(403, readable_exception(e, "Access forbidden"))
        # except api.MissingArgumentsError as e:
        #     resp = json_error_response(400, readable_exception(e, "Missing some required arguments"))
        except api.InvalidArgumentsError as e:
            resp = json_error_response(400, readable_exception(e, "Some arguments are not valid"))
        except api.ConflictError as e:
            resp = json_error_response(409, readable_exception(e, "Resource conflict"))
        except api.NotAcceptableError as e:
            resp = json_error_response(406, readable_exception(e, "Not acceptable"))
        except api.Created as e:
            resp = json_error_response(201, readable_exception(e, "Created"))
        except api.NotAuthenticatedError:
            resp = json_error_response(401, "Not authenticated")
        except api.ForceLogoutError as e:
            resp = json_error_response(200, readable_exception(e, "Disconnected"))
            resp.del_cookie("session")
        except asyncio.CancelledError:
            resp = json_error_response(400, "Request was interrupted")
        except Exception:
            # Errore non gestito
            # Stampa lo stacktrace in console
            stack_trace = str(traceback.format_exc())
            print(stack_trace)

            # Se l'api è in debug mode, invia lo stacktrace al client
            # altrimenti mostra un messaggio generico
            if EmaNews().debug:
                msg = readable_exception(traceback.format_exc(), "Unhandled internal server error")
            else:
                msg = "Internal server error."
            resp = json_error_response(500, msg)
            # TODO: Sentry
        finally:
            # Ritorna la risposta al client
            return resp
    return wrapper


def base(f: Callable) -> Callable:
    """
    Decorator che contiene i decorator base dell'api.
    Deve essere posto come primo decorator per ogni handler dell'api.

    :param f:
    :return:
    """
    return errors(f)


def args(schema_: Union[Schema, dict]) -> Callable:
    """
    Decorator che controlla gli argomenti passati ad un handler aiohttp,
    secondo uno schema passato

    :param schema_: Se viene passato un oggetto Schema, la validazione
    avverrà con quell'oggetto preciso. In caso di richiesta GET, potrebbe
    essere necessario convertire il MultiDict in dict.
    Se viene passato un dict, questo verrà passato ad uno schema che, eventualmente,
    trasforma i parametri da MultiDict a dict.
    :type: Union[Schema, dict]
    :return:
    """
    def decorator(f: Callable):
        async def wrapper(request: web.Request, *args, **kwargs):
            if request.method == "GET":
                # Metodo GET, parametri da querystring
                current_args = request.query
            else:
                # Altro metodo, leggi il JSON nella richiesta
                try:
                    current_args = await request.json()
                except json.JSONDecodeError:
                    raise api.InvalidArgumentsError("Invalid JSON data")

            if type(schema_) is dict:
                # Creazione oggetto Schema se necessario
                schema_components = [Use(multidict_to_dict)] if issubclass(type(current_args), MultiDict) else []
                schema_components += [schema_]
                schema = Schema(
                    And(*schema_components)
                )
            else:
                # Oggetto Schema già fornito
                schema = schema_

            # Verifica schema
            try:
                data = schema.validate(dict(current_args))
            except SchemaError as e:
                raise api.InvalidArgumentsError(e)

            # Schema ok, chiama handler
            return await f(request, data, *args, **kwargs)
        return wrapper
    return decorator


def protected(required_privileges: Privileges=Privileges.NORMAL) -> Callable:
    """
    Decorator che rende un handler accessibile solo se si è loggati e si dispone di
    determinati privilegi.

    :param required_privileges: Flag necessari. Il controllo avviene con un bitwise and.
    :type required_privileges: Privileges
    :return:
    """
    def decorator(f: Callable) -> Callable:
        async def wrapper(request: web.Request, *args, **kwargs) -> Response:
            session_token = request.cookies.get("session")
            if not session_token:
                raise api.NotAuthenticatedError()

            try:
                session = await sessions.SessionFactory.load_from_redis(session_token)

                async with EmaNews().db.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("SELECT privileges FROM users WHERE id = %s LIMIT 1", (session.user_id,))
                        privs = await cur.fetchone()
                        if not privs:
                            raise sessions.SessionError("User not found")
                        if not (privs["privileges"] & required_privileges):
                            raise api.ForbiddenError("Insufficient privileges")
            except sessions.SessionError as e:
                await sessions.SessionFactory.delete_from_redis(session_token)
                raise api.ForceLogoutError(e)

            return await f(session, request, *args, **kwargs)
        return wrapper
    return decorator


def guest_only(f: Callable) -> Callable:
    """
    Decorator che rende un handler accessbile solo agli utenti non loggati.

    :param f:
    :return:
    """
    async def wrapper(request: web.Request, *args, **kwargs) -> Response:
        if request.cookies.get("session"):
            raise api.ForbiddenError("You are already logged in")
        return await f(request, *args, **kwargs)
    return wrapper
