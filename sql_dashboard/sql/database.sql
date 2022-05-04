
CREATE TABLE IF NOT EXISTS `tweets` 
(
    `id` INT NOT NULL AUTO_INCREMENT,
    `created_at` TEXT DEFAULT NULL,
    `source` VARCHAR(200) DEFAULT NULL,
    `original_text` TEXT DEFAULT NULL,
    `retweet_text` TEXT DEFAULT NULL,
    `sentiment` INT DEFAULT NULL,
    `polarity` FLOAT DEFAULT NULL,
    `subjectivity` FLOAT DEFAULT NULL,
    `lang` TEXT DEFAULT NULL,
    `statuses_count` INT DEFAULT NULL,
    `favorite_count` INT DEFAULT NULL,
    `retweet_count` INT DEFAULT NULL,
    `screen_name` TEXT DEFAULT NULL,
    `followers_count` INT DEFAULT NULL,
    `friends_count` INT DEFAULT NULL,
    `possibly_sensitive` BOOLEAN DEFAULT NULL,
    `hashtags` TEXT DEFAULT NULL,
    `user_mentions` TEXT DEFAULT NULL,
    `location` TEXT DEFAULT NULL,
    PRIMARY KEY (`id`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;