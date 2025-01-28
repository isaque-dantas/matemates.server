CREATE TABLE `api_user`
(
    `id`            bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `password`      varchar(128)          NOT NULL,
    `last_login`    datetime(6)           NULL,
    `username`      varchar(32)           NOT NULL UNIQUE,
    `name`          varchar(64)           NOT NULL,
    `email`         varchar(128)          NOT NULL UNIQUE,
    `is_staff`      bool                  NOT NULL,
    `profile_image` varchar(100)          NOT NULL
);

CREATE TABLE `api_entry`
(
    `id`           bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `content`      varchar(128)          NOT NULL UNIQUE,
    `is_validated` bool                  NOT NULL
);

CREATE TABLE `api_knowledgearea`
(
    `id`      bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `content` varchar(128)          NOT NULL UNIQUE,
    `subject` varchar(128)          NOT NULL
);

CREATE TABLE `api_image`
(
    `id`                    bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `content`               varchar(100)          NOT NULL,
    `caption`               varchar(256)          NOT NULL,
    `image_number_in_entry` integer               NOT NULL,
    `entry_id`              bigint                NOT NULL
);

CREATE TABLE `api_invitedemail`
(
    `id`                  bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `email`               varchar(128)          NOT NULL UNIQUE,
    `user_who_invited_id` bigint                NOT NULL
);

CREATE TABLE `api_definition`
(
    `id`                bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `content`           varchar(256)          NOT NULL,
    `entry_id`          bigint                NOT NULL,
    `knowledge_area_id` bigint                NOT NULL
);

CREATE TABLE `api_question`
(
    `id`          bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `statement`   varchar(256)          NOT NULL,
    `answer`      varchar(256)          NOT NULL,
    `explanation` varchar(256)          NOT NULL,
    `entry_id`    bigint                NOT NULL
);

CREATE TABLE `api_term`
(
    `id`                   bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `content`              varchar(64)           NOT NULL UNIQUE,
    `gender`               varchar(16)           NOT NULL,
    `grammatical_category` varchar(16)           NOT NULL,
    `is_main_term`         bool                  NOT NULL,
    `entry_id`             bigint                NOT NULL
);

CREATE TABLE `api_syllable`
(
    `id`      bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `content` varchar(16)           NOT NULL,
    `term_id` bigint                NOT NULL
);

ALTER TABLE `api_image`
    ADD CONSTRAINT `api_image_entry_id_7287b5c0_fk_api_entry_id`
        FOREIGN KEY (`entry_id`) REFERENCES `api_entry` (`id`);

ALTER TABLE `api_invitedemail`
    ADD CONSTRAINT `api_invitedemail_user_who_invited_id_73a51900_fk_api_user_id`
        FOREIGN KEY (`user_who_invited_id`) REFERENCES `api_user` (`id`);

ALTER TABLE `api_definition`
    ADD CONSTRAINT `api_definition_entry_id_0ebeb240_fk_api_entry_id`
        FOREIGN KEY (`entry_id`) REFERENCES `api_entry` (`id`);

ALTER TABLE `api_definition`
    ADD CONSTRAINT `api_definition_knowledge_area_id_acfcfe70_fk_api_knowl`
        FOREIGN KEY (`knowledge_area_id`) REFERENCES `api_knowledgearea` (`id`);

ALTER TABLE `api_question`
    ADD CONSTRAINT `api_question_entry_id_2de877d5_fk_api_entry_id`
        FOREIGN KEY (`entry_id`) REFERENCES `api_entry` (`id`);

ALTER TABLE `api_term`
    ADD CONSTRAINT `api_term_entry_id_890d79ea_fk_api_entry_id`
        FOREIGN KEY (`entry_id`) REFERENCES `api_entry` (`id`);

ALTER TABLE `api_syllable`
    ADD CONSTRAINT `api_syllable_term_id_ab166577_fk_api_term_id`
        FOREIGN KEY (`term_id`) REFERENCES `api_term` (`id`);
