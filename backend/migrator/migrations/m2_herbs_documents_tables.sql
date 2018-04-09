CREATE TABLE `documents` (
  `id` int(11) NOT NULL,
  `herb_id` int(11) NOT NULL,
  `type` enum('consultation','other') NOT NULL,
  `name` varchar(128) NOT NULL,
  `language` varchar(64) NOT NULL,
  `first_published` varchar(16) NOT NULL,
  `last_updated_ema` varchar(16) NOT NULL,
  `url` varchar(255) NOT NULL,
  `latest_update` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `herbs` (
  `id` int(11) NOT NULL,
  `latin_name` varchar(128) NOT NULL,
  `botanic_name` varchar(128) NOT NULL,
  `english_name` varchar(128) NOT NULL,
  `status` enum('R','C','D','P','PF','F') NOT NULL,
  `url` varchar(255) NOT NULL,
  `latest_update` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `documents`
  ADD PRIMARY KEY (`id`),
  ADD KEY `documents_ibfk_1` (`herb_id`);

ALTER TABLE `herbs`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `documents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `herbs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `documents`
  ADD CONSTRAINT `documents_ibfk_1` FOREIGN KEY (`herb_id`) REFERENCES `herbs` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;