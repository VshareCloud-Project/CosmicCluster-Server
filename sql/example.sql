-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2023-05-20 14:01:00
-- 服务器版本： 10.5.6-MariaDB-log
-- PHP 版本： 7.4.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `ysf-test`
--

-- --------------------------------------------------------

--
-- 表的结构 `admin_node`
--

CREATE TABLE `admin_node` (
  `id` bigint(20) NOT NULL,
  `uuid` varchar(68) NOT NULL,
  `keychain` varchar(5000) DEFAULT NULL,
  `name` varchar(200) NOT NULL DEFAULT '',
  `last_seen` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `dnode`
--

CREATE TABLE `dnode` (
  `id` bigint(20) NOT NULL,
  `uuid` varchar(68) NOT NULL,
  `keychain` varchar(5000) DEFAULT NULL,
  `name` varchar(200) NOT NULL DEFAULT '',
  `cpus` int(11) NOT NULL DEFAULT 0,
  `memory` bigint(20) NOT NULL DEFAULT 0,
  `storage` bigint(20) NOT NULL DEFAULT 0,
  `disk_info` varchar(5000) NOT NULL,
  `last_seen` datetime NOT NULL DEFAULT current_timestamp(),
  `is_offical_node` int(2) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `dnode_status_log`
--

CREATE TABLE `dnode_status_log` (
  `id` bigint(20) NOT NULL,
  `node_id` varchar(68) NOT NULL,
  `percent_cpu` float NOT NULL,
  `percent_mem` float NOT NULL,
  `percent_disk` float NOT NULL,
  `disk_info` varchar(5000) NOT NULL,
  `update_time` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转储表的索引
--

--
-- 表的索引 `admin_node`
--
ALTER TABLE `admin_node`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- 表的索引 `dnode`
--
ALTER TABLE `dnode`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uuid` (`uuid`);

--
-- 表的索引 `dnode_status_log`
--
ALTER TABLE `dnode_status_log`
  ADD PRIMARY KEY (`id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `admin_node`
--
ALTER TABLE `admin_node`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `dnode`
--
ALTER TABLE `dnode`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `dnode_status_log`
--
ALTER TABLE `dnode_status_log`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
