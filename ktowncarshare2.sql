-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 12, 2018 at 06:23 PM
-- Server version: 10.1.29-MariaDB
-- PHP Version: 7.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ktowncarshare2`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_reply`
--

CREATE TABLE `admin_reply` (
  `adminReplyID` char(11) NOT NULL,
  `commentID` char(11) NOT NULL,
  `adminReplyText` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin_reply`
--

INSERT INTO `admin_reply` (`adminReplyID`, `commentID`, `adminReplyText`) VALUES
('Reply123456', 'Comment2345', 'You will pay for this');

-- --------------------------------------------------------

--
-- Table structure for table `car`
--

CREATE TABLE `car` (
  `VIN` int(11) NOT NULL,
  `carTypeID` char(11) NOT NULL,
  `parkingAddress` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `car`
--

INSERT INTO `car` (`VIN`, `carTypeID`, `parkingAddress`) VALUES
(12345, 'PontSun1', '99 University Avenue'),
(23456, 'ToyCor1', '802 High Gate Park Drive');

-- --------------------------------------------------------

--
-- Table structure for table `car_maintenance_history`
--

CREATE TABLE `car_maintenance_history` (
  `maintenanceID` char(11) NOT NULL,
  `memberID` char(11) NOT NULL,
  `VIN` int(11) NOT NULL,
  `date` date NOT NULL,
  `cost` int(11) NOT NULL,
  `kmOdometer` int(11) NOT NULL,
  `maintenanceType` varchar(50) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `car_maintenance_history`
--

INSERT INTO `car_maintenance_history` (`maintenanceID`, `memberID`, `VIN`, `date`, `cost`, `kmOdometer`, `maintenanceType`, `description`) VALUES
('maint12345', '10000000000', 23456, '2018-04-11', 2000, 1000, 'fix engine', 'car was not running, had to fix engine');

-- --------------------------------------------------------

--
-- Table structure for table `car_rental_history`
--

CREATE TABLE `car_rental_history` (
  `reservationID` char(11) NOT NULL,
  `memberID` char(11) NOT NULL,
  `pickUpKm` int(11) NOT NULL,
  `dropOffKm` int(11) DEFAULT NULL,
  `statusOnPickup` varchar(100) DEFAULT NULL,
  `statusOnReturn` varchar(100) DEFAULT NULL,
  `pickUpTime` datetime DEFAULT NULL,
  `dropOffTime` datetime DEFAULT NULL,
  `VIN` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `car_rental_history`
--

INSERT INTO `car_rental_history` (`reservationID`, `memberID`, `pickUpKm`, `dropOffKm`, `statusOnPickup`, `statusOnReturn`, `pickUpTime`, `dropOffTime`, `VIN`) VALUES
('Reserve1234', '10000000000', 2015, 2026, 'good', 'good', '2018-04-09 16:00:00', '2018-04-09 19:00:00', 12345),
('Reserve2345', '10000000000', 1, 1000, 'normal', 'not running', '2018-03-29 16:00:00', '2018-04-10 20:30:00', 23456);

-- --------------------------------------------------------

--
-- Table structure for table `car_type`
--

CREATE TABLE `car_type` (
  `carTypeID` char(11) NOT NULL,
  `make` varchar(100) DEFAULT NULL,
  `model` varchar(100) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `dailyRentalFee` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `car_type`
--

INSERT INTO `car_type` (`carTypeID`, `make`, `model`, `year`, `dailyRentalFee`) VALUES
('PontSun1', 'Pontiac', 'Sunfire', 1996, 20),
('PontSun2', 'Pontiac', 'Sunfire', 2015, 200),
('ToyCor1', 'Toyota', 'Corolla', 1997, 30);

-- --------------------------------------------------------

--
-- Table structure for table `member`
--

CREATE TABLE `member` (
  `memberID` char(11) NOT NULL,
  `FName` varchar(30) DEFAULT NULL,
  `LName` varchar(30) NOT NULL,
  `address` varchar(100) DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `driverLicenseNum` varchar(100) NOT NULL,
  `monthlyMemberFee` int(11) NOT NULL,
  `password` varchar(65) NOT NULL,
  `isAdmin` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `member`
--

INSERT INTO `member` (`memberID`, `FName`, `LName`, `address`, `phone`, `email`, `driverLicenseNum`, `monthlyMemberFee`, `password`, `isAdmin`) VALUES
('10000000000', 'Chris', 'Dean', '900 High Gate Park Drive', 1136340017, 'cjd1618@gmail.com', 'D2737-12457-60714', 1, 'ChrisPassword', 0);

-- --------------------------------------------------------

--
-- Table structure for table `member_rental_history`
--

CREATE TABLE `member_rental_history` (
  `reservationID` char(11) NOT NULL,
  `memberID` char(11) NOT NULL,
  `VIN` int(11) NOT NULL,
  `rentalDate` date NOT NULL,
  `accessCode` char(11) DEFAULT NULL,
  `reservationNumDays` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `member_rental_history`
--

INSERT INTO `member_rental_history` (`reservationID`, `memberID`, `VIN`, `rentalDate`, `accessCode`, `reservationNumDays`) VALUES
('Reserve1234', '10000000000', 12345, '2017-03-08', 'LetMeIn', 3),
('Reserve2345', '10000000000', 23456, '2017-03-24', 'LetThemIn', 1);

-- --------------------------------------------------------

--
-- Table structure for table `parking_locations`
--

CREATE TABLE `parking_locations` (
  `parkingAddress` varchar(100) NOT NULL,
  `numSpaces` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `parking_locations`
--

INSERT INTO `parking_locations` (`parkingAddress`, `numSpaces`) VALUES
('802 High Gate Park Drive', 14),
('99 University Avenue', 77);

-- --------------------------------------------------------

--
-- Table structure for table `rental_comments`
--

CREATE TABLE `rental_comments` (
  `commentID` char(11) NOT NULL,
  `memberID` char(11) NOT NULL,
  `reservationID` char(11) NOT NULL,
  `VIN` int(11) NOT NULL,
  `rating` int(11) DEFAULT NULL,
  `commentText` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rental_comments`
--

INSERT INTO `rental_comments` (`commentID`, `memberID`, `reservationID`, `VIN`, `rating`, `commentText`) VALUES
('Comment1234', '10000000000', 'Reserve1234', 12345, 10, 'Smooth ride. Good Car. Love Sunny.'),
('Comment2345', '10000000000', 'Reserve2345', 23456, 1, 'Sorry about that.');

-- --------------------------------------------------------

--
-- Table structure for table `reservations`
--

CREATE TABLE `reservations` (
  `reservationID` char(11) NOT NULL,
  `memberID` char(11) NOT NULL,
  `VIN` int(11) NOT NULL,
  `rentalDate` date NOT NULL,
  `accessCode` char(11) DEFAULT NULL,
  `reservationNumDays` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `reservations`
--

INSERT INTO `reservations` (`reservationID`, `memberID`, `VIN`, `rentalDate`, `accessCode`, `reservationNumDays`) VALUES
('Reserve1234', '10000000000', 12345, '2017-03-08', 'LetMeIn', 3),
('Reserve2345', '10000000000', 23456, '2017-03-24', 'LetThemIn', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_reply`
--
ALTER TABLE `admin_reply`
  ADD PRIMARY KEY (`adminReplyID`),
  ADD KEY `commentID` (`commentID`);

--
-- Indexes for table `car`
--
ALTER TABLE `car`
  ADD PRIMARY KEY (`VIN`),
  ADD KEY `parkingAddress` (`parkingAddress`),
  ADD KEY `carTypeID` (`carTypeID`);

--
-- Indexes for table `car_maintenance_history`
--
ALTER TABLE `car_maintenance_history`
  ADD PRIMARY KEY (`maintenanceID`),
  ADD KEY `memberID` (`memberID`),
  ADD KEY `VIN` (`VIN`);

--
-- Indexes for table `car_rental_history`
--
ALTER TABLE `car_rental_history`
  ADD PRIMARY KEY (`reservationID`),
  ADD KEY `memberID` (`memberID`),
  ADD KEY `VIN` (`VIN`);

--
-- Indexes for table `car_type`
--
ALTER TABLE `car_type`
  ADD PRIMARY KEY (`carTypeID`);

--
-- Indexes for table `member`
--
ALTER TABLE `member`
  ADD PRIMARY KEY (`memberID`);

--
-- Indexes for table `member_rental_history`
--
ALTER TABLE `member_rental_history`
  ADD PRIMARY KEY (`reservationID`),
  ADD KEY `memberID` (`memberID`),
  ADD KEY `VIN` (`VIN`);

--
-- Indexes for table `parking_locations`
--
ALTER TABLE `parking_locations`
  ADD PRIMARY KEY (`parkingAddress`);

--
-- Indexes for table `rental_comments`
--
ALTER TABLE `rental_comments`
  ADD PRIMARY KEY (`commentID`),
  ADD KEY `memberID` (`memberID`),
  ADD KEY `VIN` (`VIN`);

--
-- Indexes for table `reservations`
--
ALTER TABLE `reservations`
  ADD PRIMARY KEY (`reservationID`),
  ADD KEY `memberID` (`memberID`),
  ADD KEY `VIN` (`VIN`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `admin_reply`
--
ALTER TABLE `admin_reply`
  ADD CONSTRAINT `admin_reply_ibfk_1` FOREIGN KEY (`commentID`) REFERENCES `rental_comments` (`commentID`);

--
-- Constraints for table `car`
--
ALTER TABLE `car`
  ADD CONSTRAINT `car_ibfk_1` FOREIGN KEY (`parkingAddress`) REFERENCES `parking_locations` (`parkingAddress`),
  ADD CONSTRAINT `car_ibfk_2` FOREIGN KEY (`carTypeID`) REFERENCES `car_type` (`carTypeID`);

--
-- Constraints for table `car_maintenance_history`
--
ALTER TABLE `car_maintenance_history`
  ADD CONSTRAINT `car_maintenance_history_ibfk_1` FOREIGN KEY (`memberID`) REFERENCES `member` (`memberID`),
  ADD CONSTRAINT `car_maintenance_history_ibfk_2` FOREIGN KEY (`VIN`) REFERENCES `car` (`VIN`);

--
-- Constraints for table `car_rental_history`
--
ALTER TABLE `car_rental_history`
  ADD CONSTRAINT `car_rental_history_ibfk_1` FOREIGN KEY (`memberID`) REFERENCES `member` (`memberID`),
  ADD CONSTRAINT `car_rental_history_ibfk_2` FOREIGN KEY (`VIN`) REFERENCES `car` (`VIN`);

--
-- Constraints for table `member_rental_history`
--
ALTER TABLE `member_rental_history`
  ADD CONSTRAINT `member_rental_history_ibfk_1` FOREIGN KEY (`memberID`) REFERENCES `member` (`memberID`),
  ADD CONSTRAINT `member_rental_history_ibfk_2` FOREIGN KEY (`VIN`) REFERENCES `car` (`VIN`);

--
-- Constraints for table `rental_comments`
--
ALTER TABLE `rental_comments`
  ADD CONSTRAINT `rental_comments_ibfk_1` FOREIGN KEY (`memberID`) REFERENCES `member` (`memberID`),
  ADD CONSTRAINT `rental_comments_ibfk_2` FOREIGN KEY (`VIN`) REFERENCES `car` (`VIN`);

--
-- Constraints for table `reservations`
--
ALTER TABLE `reservations`
  ADD CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`memberID`) REFERENCES `member` (`memberID`),
  ADD CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`VIN`) REFERENCES `car` (`VIN`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
