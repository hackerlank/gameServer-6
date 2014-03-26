-- 2014-03-26
CREATE TABLE games(
	id INT(10) NOT NULL AUTO_INCREMENT,
	gameCode VARCHAR(60) NOT NULL DEFAULT '' COMMENT 'gameCode',
	gameName VARCHAR(60) NOT NULL DEFAULT '' COMMENT 'gameName',
	`version` VARCHAR(60) NOT NULL DEFAULT '' COMMENT 'version',
	`date` INT(10) NOT NULL DEFAULT 0 COMMENT '日期',
	bz INT(1) NOT NULL DEFAULT 1 COMMENT '0 - 不可用 1 - 可用',
	PRIMARY KEY(id)
);