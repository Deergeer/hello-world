-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: 2017-06-21 01:38:56
-- 服务器版本： 5.7.14
-- PHP Version: 5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dean`
--

-- --------------------------------------------------------

--
-- 表的结构 `choose`
--

CREATE TABLE `choose` (
  `personid` varchar(20) COLLATE utf8_bin NOT NULL,
  `teachid` int(11) NOT NULL,
  `grade1` int(11) DEFAULT '0',
  `grade2` int(11) DEFAULT '0',
  `grade3` int(11) DEFAULT '0',
  `grade` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- 转存表中的数据 `choose`
--

INSERT INTO `choose` (`personid`, `teachid`, `grade1`, `grade2`, `grade3`, `grade`) VALUES
('1300010001', 2, 100, 60, 100, 88);

-- --------------------------------------------------------

--
-- 表的结构 `course`
--

CREATE TABLE `course` (
  `id` varchar(20) COLLATE utf8_bin NOT NULL,
  `name` varchar(50) COLLATE utf8_bin NOT NULL,
  `credit` int(5) NOT NULL,
  `description` varchar(255) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- 转存表中的数据 `course`
--

INSERT INTO `course` (`id`, `name`, `credit`, `description`) VALUES
('00', 'Python程序设计', 3, '学习Python语言，设计程序。'),
('01', '计算机网络', 3, '学习计算机通讯架构。'),
('10', '语文', 2, '学习中国语言文学。'),
('11', '英语', 2, '听说读写'),
('12', '古代汉语', 1, '古代中国语言文学');

-- --------------------------------------------------------

--
-- 表的结构 `person`
--

CREATE TABLE `person` (
  `id` varchar(20) COLLATE utf8_bin NOT NULL,
  `password` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT '666666',
  `name` varchar(20) COLLATE utf8_bin NOT NULL,
  `role` varchar(20) COLLATE utf8_bin NOT NULL,
  `description` varchar(255) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- 转存表中的数据 `person`
--

INSERT INTO `person` (`id`, `password`, `name`, `role`, `description`) VALUES
('10001', 'Bb111111', '李四', '教务员', '教务办公室老师'),
('10240001', 'Aa000000', '王五', '教师', '研究方向：python，博士学位。'),
('10240002', '666666', '赵六', '教师', '中文系教授'),
('1300010001', 'Aa000000', '张三', '学生', '计算机系13级本科生，热爱编程。'),
('1300010002', '666666', '王明', '学生', '');

-- --------------------------------------------------------

--
-- 表的结构 `teach`
--

CREATE TABLE `teach` (
  `id` int(11) NOT NULL,
  `teacherid` varchar(20) COLLATE utf8_bin NOT NULL,
  `courseid` varchar(20) COLLATE utf8_bin NOT NULL,
  `percent1` int(11) NOT NULL,
  `percent2` int(11) NOT NULL,
  `percent3` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- 转存表中的数据 `teach`
--

INSERT INTO `teach` (`id`, `teacherid`, `courseid`, `percent1`, `percent2`, `percent3`) VALUES
(2, '10240001', '00', 20, 30, 50),
(3, '10240001', '01', 20, 20, 60);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Indexes for table `person`
--
ALTER TABLE `person`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `teach`
--
ALTER TABLE `teach`
  ADD PRIMARY KEY (`id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `teach`
--
ALTER TABLE `teach`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
