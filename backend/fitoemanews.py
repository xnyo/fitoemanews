from singletons.config import Config
from singletons.emanews import EmaNews


def main():
    c = Config()
    EmaNews(
        db_host=c["DB_HOST"],
        db_port=c["DB_PORT"],
        db_username=c["DB_USERNAME"],
        db_password=c["DB_PASSWORD"],
        db_database=c["DB_NAME"],
        db_pool_minsize=c["DB_POOL_MIN_SIZE"],
        db_pool_maxsize=c["DB_POOL_MAX_SIZE"],
        debug=c["DEBUG"],
        web_host=c["HTTP_HOST"],
        web_port=c["HTTP_PORT"]
    ).start()


if __name__ == '__main__':
    main()
