/*
Navicat SQLite Data Transfer

Source Server         : 工时系统
Source Server Version : 30808
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 30808
File Encoding         : 65001

Date: 2019-03-11 10:14:24
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
DROP TABLE IF EXISTS "main"."sqlite_sequence";
CREATE TABLE sqlite_sequence(name,seq);

-- ----------------------------
-- Table structure for t_company
-- ----------------------------
DROP TABLE IF EXISTS "main"."t_company";
CREATE TABLE "t_company" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"name"  TEXT NOT NULL,
"status"  INTEGER NOT NULL DEFAULT 0,
"logo_file"  TEXT,
"jindee_id"  INTEGER,
FOREIGN KEY ("jindee_id") REFERENCES "t_jindee" ("id"),
UNIQUE ("name" ASC)
);

-- ----------------------------
-- Table structure for t_department
-- ----------------------------
DROP TABLE IF EXISTS "main"."t_department";
CREATE TABLE "t_department" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" TEXT NOT NULL,
  "status" INTEGER NOT NULL DEFAULT 0,
  "regtime" TEXT,
  "company_id" INTEGER NOT NULL,
  CONSTRAINT "fkey0" FOREIGN KEY ("company_id") REFERENCES "t_company" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("name" ASC, "company_id" ASC)
);

-- ----------------------------
-- Table structure for t_ic_item_header
-- ----------------------------
DROP TABLE IF EXISTS "main"."t_ic_item_header";
CREATE TABLE "t_ic_item_header" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"project_id"  TEXT NOT NULL,
"file_name"  TEXT NOT NULL,
"file_id"  TEXT NOT NULL,
"item_num"  TEXT,
"version"  TEXT NOT NULL,
"user_id"  INTEGER NOT NULL,
"auditing"  TEXT,
"proofreading"  TEXT,
"approval"  TEXT,
"signer"  TEXT,
"date"  TEXT NOT NULL,
CONSTRAINT "fkey0" FOREIGN KEY ("project_id") REFERENCES "t_project" ("id"),
FOREIGN KEY ("user_id") REFERENCES "t_user" ("id")
);

-- ----------------------------
-- Table structure for t_item_detail
-- ----------------------------
DROP TABLE IF EXISTS "main"."t_item_detail";
CREATE TABLE "t_item_detail" (
"id"  INTEGER NOT NULL,
"index"  INTEGER NOT NULL,
"item_number"  TEXT NOT NULL,
"name"  TEXT,
"model"  TEXT NOT NULL,
"note"  TEXT,
"install_number"  TEXT,
"unit"  TEXT NOT NULL,
"number"  INTEGER NOT NULL,
"remark"  TEXT,
"ic_item_header_id"  INTEGER NOT NULL,
PRIMARY KEY ("id" ASC),
FOREIGN KEY ("ic_item_header_id") REFERENCES "t_ic_item_header" ("id"),
UNIQUE ("index" ASC, "ic_item_header_id" ASC)
);

-- ----------------------------
-- Table structure for t_jindee
-- ----------------------------
DROP TABLE IF EXISTS "main"."t_jindee";
CREATE TABLE "t_jindee" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"name"  TEXT NOT NULL,
"userName"  TEXT NOT NULL,
"userPw"  TEXT NOT NULL,
"DBAddress"  TEXT NOT NULL,
"DBName"  TEXT NOT NULL
);

-- ----------------------------
-- Table structure for t_project
-- ----------------------------
DROP TABLE IF EXISTS "main"."t_project";
CREATE TABLE "t_project" (
  "id" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  "status" INTEGER NOT NULL DEFAULT 0,
  "regtime" TEXT NOT NULL,
  "department_id" INTEGER NOT NULL,
  "super_user_id" INtEGER NOT NULL,
  PRIMARY KEY ("id"),
  CONSTRAINT "fkey0" FOREIGN KEY ("department_id") REFERENCES "t_department" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("super_user_id") REFERENCES "t_user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("name" ASC, "department_id" ASC),
  UNIQUE ("id" ASC)
);

-- ----------------------------
-- Table structure for t_project_user
-- ----------------------------
DROP TABLE IF EXISTS "main"."t_project_user";
CREATE TABLE "t_project_user" (
  "user_id" INTEGER NOT NULL,
  "project_id" TEXT NOT NULL,
  "status" INTEGER DEFAULT 0,
  "addtime" TEXT,
  CONSTRAINT "fkey0" FOREIGN KEY ("user_id") REFERENCES "t_user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT "fkey1" FOREIGN KEY ("project_id") REFERENCES "t_project" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("user_id" ASC, "project_id" ASC)
);

-- ----------------------------
-- Table structure for t_user
-- ----------------------------
DROP TABLE IF EXISTS "main"."t_user";
CREATE TABLE "t_user" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "user" TEXT NOT NULL,
  "pw" TEXT NOT NULL,
  "status" INTEGER NOT NULL DEFAULT 0,
  "regtime" TEXT NOT NULL,
  "department_id" INTEGER NOT NULL,
  "company_id" INTEGER DEFAULT 1,
  CONSTRAINT "fkey0" FOREIGN KEY ("department_id") REFERENCES "t_department" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("company_id") REFERENCES "t_company" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("user" ASC)
);

-- ----------------------------
-- Table structure for t_work_record
-- ----------------------------
DROP TABLE IF EXISTS "main"."t_work_record";
CREATE TABLE "t_work_record" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"user_id"  INTEGER NOT NULL,
"project_id"  TEXT NOT NULL,
"worktime"  REAL NOT NULL,
"date"  TEXT NOT NULL,
"time"  TEXT,
"status"  INTEGER NOT NULL DEFAULT 1,
CONSTRAINT "fkey0" FOREIGN KEY ("user_id") REFERENCES "t_user" ("id"),
CONSTRAINT "fkey1" FOREIGN KEY ("project_id") REFERENCES "t_project" ("id"),
UNIQUE ("user_id" ASC, "project_id" ASC, "date" ASC)
);

-- ----------------------------
-- View structure for v_item_table
-- ----------------------------
DROP VIEW IF EXISTS "main"."v_item_table";
CREATE VIEW "v_item_table" AS SELECT t_ic_item_header.*,t_user.user as user_name ,t_project.name as project_name
FROM t_ic_item_header,t_user,t_project
WHERE t_ic_item_header.user_id = t_user.id and t_ic_item_header.project_id = t_project.id;
