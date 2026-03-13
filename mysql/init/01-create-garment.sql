USE gtdb;

CREATE TABLE IF NOT EXISTS garment (
    id_garment INT(11) NOT NULL AUTO_INCREMENT,
    rfid_garment VARCHAR(36) NOT NULL,
    item VARCHAR(30) NOT NULL,
    buyer VARCHAR(30) NOT NULL,
    style VARCHAR(30) NOT NULL,
    wo VARCHAR(30) NOT NULL,
    color VARCHAR(30) NOT NULL,
    size VARCHAR(30) NOT NULL,
    branch VARCHAR(10) NOT NULL,
    isDone VARCHAR(30) NOT NULL,
    `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    isMove VARCHAR(30) NOT NULL,
    PRIMARY KEY (id_garment),
    KEY idx_rfid_garment (rfid_garment),
    KEY idx_isDone (isDone),
    KEY idx_timestamp (`timestamp`),
    KEY idx_isMove (isMove)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;