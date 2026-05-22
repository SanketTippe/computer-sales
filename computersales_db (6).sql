-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 28, 2025 at 10:16 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `computersales_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_addcategory`
--

CREATE TABLE `tbl_addcategory` (
  `id` int(9) NOT NULL,
  `category_name` varchar(50) NOT NULL,
  `category_image` varchar(100) NOT NULL,
  `description` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_addcategory`
--

INSERT INTO `tbl_addcategory` (`id`, `category_name`, `category_image`, `description`) VALUES
(28, 'ASUS', 'static/uploads\\as8.jpg', 'Asus computers are known for their exceptional performance, innovative features, and sleek designs. '),
(30, 'HP', 'static/uploads\\hp8.jpg', 'HP computers offer a wide range of reliable and high-performance devices, from laptops to desktops. '),
(32, 'DELL', 'static/uploads\\Dell5.jpg', 'Dell computers are known for their powerful performance, sleek designs, and customization options.  '),
(34, 'APPLE', 'static/uploads\\ap9.jpg', 'Apple computers combine cutting-edge technology with elegant design, offering seamless performance. ');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_addproduct`
--

CREATE TABLE `tbl_addproduct` (
  `id` int(9) NOT NULL,
  `product_name` varchar(50) NOT NULL,
  `brand` varchar(50) NOT NULL,
  `price` double NOT NULL,
  `quantity` varchar(50) NOT NULL,
  `description` varchar(100) NOT NULL,
  `category` varchar(20) NOT NULL,
  `product_image` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_addproduct`
--

INSERT INTO `tbl_addproduct` (`id`, `product_name`, `brand`, `price`, `quantity`, `description`, `category`, `product_image`) VALUES
(15, 'Laptop', 'ASUS', 50000, '1', 'TUF Gaming F15 AI Powered Gaming Laptop, Intel Core i5-11400H 11th Gen.', 'asus', 'static/uploads\\as1.jpg'),
(17, 'Laptop', 'ASUS', 88000, '1', 'ROG Strix G17 (2022), 17.3-inch (43.94 cms) FHD 144Hz.', 'asus', 'static/uploads\\as3.jpg'),
(18, 'Laptop', 'ASUS', 114000, '1', '14 Flip OLED (2023), Intel Core EVO i7-1360P 13th Gen.', 'asus', 'static/uploads\\as4.jpg'),
(19, 'Laptop', 'ASUS', 78000, '1', 'S15 OLED 2022, 15.6\" 39.62 cms FHD OLED, Intel Core Evo i7-12700H 12th Gen.', 'asus', 'static/uploads\\as5.jpg'),
(20, 'Laptop', 'ASUS', 17000, '1', 'Laptop, 11.6\" (29.46cm) HD Anti-Glare Display, Intel Celeron N4500.', 'asus', 'static/uploads\\as6.jpg'),
(22, 'Laptop', 'ASUS', 56000, '1', '16X (2022), AMD Ryzen 7 5800Hs, 16\" (40.64 Cms) Fhd+Thin.', 'asus', 'static/uploads\\as7.jpg'),
(23, 'Laptop', 'ASUS', 46000, '1', '(2022), 16.0-inch (40.64 cms) FHD+ 16:10, AMD Ryzen 5 5600H.', 'asus', 'static/uploads\\as8.jpg'),
(24, 'Laptop', 'ASUS', 72000, '1', 'Vivobook Pro 15, AMD Ryzen 7 6800HS, 15.6\" (39.62 cm) FHD, Creator Laptop.', 'asus', 'static/uploads\\as10.jpg'),
(25, 'Laptop', 'HP', 35000, '1', '11th Gen Intel Core i3-1115G4, 14-inch, FHD, 8GB DDR4, 512GB SSD.', 'HP', 'static/uploads\\hp1.jpg'),
(26, 'Laptop', 'HP', 70000, '1', '13th Gen Intel Core i5-1340P 15.6 inch FHD IPS (16GB RAM /512GB SSD.', 'HP', 'static/uploads\\hp5.jpg'),
(27, 'Laptop', 'HP', 67000, '1', '13th Gen Intel Core i5-1335U, 15.6-inch, FHD, 8GB DDR4, 1TB SSD.', 'HP', 'static/uploads\\hp5.jpg'),
(28, 'Laptop', 'HP', 58000, '1', '12th Gen Intel Core i3-1215U 8GB RAM/512GB SSD 14-inch FHD.', 'HP', 'static/uploads\\hp7.jpg'),
(29, 'Laptop', 'HP', 66000, '1', 'Gaming Laptop 12th Gen Intel Core i5-12450H 15.6 inch FHD.', 'HP', 'static/uploads\\hp8.jpg'),
(30, 'Laptop', 'HP', 81000, '1', 'x360 2-in-1 Laptop 12th Gen Intel Core i5 8GB RAM 512 SSD.', 'HP', 'static/uploads\\hp9_.jpg'),
(31, 'Laptop', 'HP', 61000, '1', '13th Gen Intel Core i5-1335U, 15.6-inch, 16GB DDR4, 512GB SSD.', 'HP', 'static/uploads\\hp12.jpg'),
(33, 'Laptop', 'HP', 42000, '1', 'AMD Ryzen 5 7520U, 15.6-inch, FHD, 8GB LPDDR5, 512GB SSD.', 'HP', 'static/uploads\\hp11.jpg'),
(34, 'Laptop', 'DELL', 49000, '1', 'Intel Core i5-1135G7 Processor/16GB DDR4/512GB SSD.', 'DELL', 'static/uploads\\Dell1.jpg'),
(35, 'Laptop', 'DELL', 69000, '1', '3530 Laptop, 13th Gen Intel Core i5-1335U Processor/16GB/1TB SSD.', 'DELL', 'static/uploads\\Dell2.jpg'),
(36, 'Laptop', 'DELL', 76000, '1', '5520 Gaming Laptop, Intel i5-12500H/16GB DDR5/1TB SSD/15.6.', 'DELL', 'static/uploads\\Dell3.jpg'),
(37, 'Laptop', 'DELL', 86000, '1', '7420 2in1 Laptop, Intel i7-1255U, 16GB DDR4 & 512GB SSD.', 'DELL', 'static/uploads\\Dell8.jpg'),
(38, 'Laptop', 'DELL', 116000, '1', 'Gaming 13th Gen Laptop, Intel i7/32GB/1TB SSD/NVIDIA RTX 4060.', 'DELL', 'static/uploads\\Dell7.jpg'),
(39, 'Laptop', 'DELL', 96000, '1', '7430 2in1 Touch, Intel Core i7-1355U Processor/16GB/512GB SSD.', 'DELL', 'static/uploads\\Dell6.jpg'),
(40, 'Laptop', 'DELL', 36000, '1', '3525 Laptop, AMD Ryzen R3-5300U/8GB/512GB SSD/15.6.', 'DELL', 'static/uploads\\Dell5.jpg'),
(41, 'Laptop', 'DELL', 126000, '1', 'Gaming 13th Gen Laptop, i7-13650HX Processor/16GB/512GB SSD.', 'DELL', 'static/uploads\\Dell4.jpg'),
(42, 'Laptop', 'APPLE', 126000, '1', 'Air Laptop (15.3-inch) Liquid Retina Display, 8GB RAM, 256GB SSD.', 'apple', 'static/uploads\\ap1.jpg'),
(43, 'Laptop', 'APPLE', 199000, '1', '14-inch, M3 chip with 8‑core CPU and 10‑core GPU, 8GB, 1TB.', 'apple', 'static/uploads\\ap2.jpg'),
(44, 'Laptop', 'APPLE', 154000, '1', 'Laptop (15.3 inch) Liquid Retina Display, 8GB RAM 512GB SSD.', 'apple', 'static/uploads\\ap3.jpg'),
(45, 'Laptop', 'APPLE', 187000, '1', 'Laptop 14.2-inch/33.74 cm Retina Display, 18GB RAM, 512GB SSD.', 'apple', 'static/uploads\\ap4.jpg'),
(46, 'Laptop', 'APPLE', 287000, '1', 'MacBook Pro12‑core CPU and 18‑core GPU, 36GB, 512GB.', 'apple', 'static/uploads\\ap5.jpg'),
(47, 'Laptop', 'APPLE', 287000, '1', 'Laptop (13.6-inch) Liquid Retina Display, 8GB RAM, 512GB SSD.', 'apple', 'static/uploads\\ap6.jpg'),
(48, 'Laptop', 'APPLE', 349000, '1', 'MacBook Pro (16-inch, 14‑core CPU and 30‑core GPU, 36GB , 1TB.', 'apple', 'static/uploads\\ap7.jpg'),
(49, 'Laptop', 'APPLE', 188000, '1', 'Pro Laptop 12‑core CPU (14.2-inch), 32GB Unified Memory, 1TB SSD.', 'apple', 'static/uploads\\ap8.jpg'),
(51, 'Desktop', 'HP', 59000, '1', 'HP All-in-One PC 12th Gen Intel Core i5-1235U 24-inch(60.5 cm) 8GB RAM/512GB.', 'HP', 'static/uploads\\hpc1.jpg'),
(52, 'Desktop', 'HP', 33000, '1', 'HP All-in-One PC, Windows 11 Home, Intel Processor N200, 21.45-Inch.', 'HP', 'static/uploads\\hpc3.jpg'),
(57, 'Desktop', 'HP', 106000, '1', 'Intel Core I7 13700T,27\" Fhd 3 Sided Micro-Edge Display/16Gb Ram/1Tb SSD.', 'HP', 'static/uploads\\hpc7.jpg'),
(58, 'Desktop', 'HP', 59000, '1', 'HP PC 12th Gen Intel Core i5-1235U 24-inch FHD Anti Glare Desktop 8GB RAM/512GB.', 'HP', 'static/uploads\\hpc2.jpg'),
(59, 'Desktop', 'HP', 60000, '1', 'HP Desktop 24 PC, AMD Ryzen 5 7520U, 16 GB LPDDR5, 512GB SSD.', 'HP', 'static/uploads\\hpc9.jpg'),
(60, 'Desktop', 'HP', 60000, '1', 'HP 13th Gen Intel Core i3-1315U, 27inch FHD, Three-Sided Micro-Edge,8 GB, 512GB SSD.', 'HP', 'static/uploads\\hpc11.jpg'),
(61, 'Desktop', 'HP', 106000, '1', 'Intel Core I7 13700T,27\" Fhd 3 Sided Micro-Edge Display/16Gb Ram/1Tb SSD.', 'HP', 'static/uploads\\hpc7.jpg'),
(62, 'Desktop', 'HP', 61000, '1', 'HP Desktop 24 PC, AMD Ryzen 5 7520U, 16 GB LPDDR5, 512GB SSD.', 'HP', 'static/uploads\\hpc9.jpg'),
(63, 'Desktop', 'DELL', 61000, '1', 'Dell 24\" All-in-One PC (5420), 13th Gen Intel i5-1335U, 8GB DDR4, 512GB SSD.', 'DELL', 'static/uploads\\dellc.jpg'),
(64, 'Desktop', 'DELL', 66000, '1', 'Dell Inspiron 24 AIO (5430) Intel Processor-i5-1334U 8GB 512GB SSD.', 'dell', 'static/uploads\\dellc1.jpg'),
(65, 'Desktop', 'DELL', 91000, '1', 'Dell AIO Inspiron 5430, Core 7 150U, 16 GB, 1TB SSD Intel.', 'dell', 'static/uploads\\dellc2.jpg'),
(66, 'Desktop', 'DELL', 118000, '1', '\r\nDell 24\" All-in-One PC (5420), 13th Gen Intel i7-1355U, 16GB DDR4, 1TB SSD.', 'dell', 'static/uploads\\dellc3.jpg'),
(67, 'Desktop', 'DELL', 75000, '1', 'Dell Optiplex 9020 19\" HD Desktop Computer Set Intel Core i3 4th Gen 8 GB RAM 500 GB.', 'dell', 'static/uploads\\dellc4.jpg'),
(68, 'Desktop', 'DELL', 108000, '1', 'Dell AIO Inspiron 7730, i7-1335U, 16 GB, 1TB SSD, 27\" FHD, 60Hz.', 'dell', 'static/uploads\\dellc5.jpg'),
(69, 'Desktop', 'DELL', 20000, '1', 'Dell Optiplex 19\" HD Desktop Computer Set Intel i5 2nd Gen 8 GB RAM 500 GB HDD.', 'dell', 'static/uploads\\dellc6.jpg'),
(71, 'Desktop', 'DELL', 20000, '1', ' Inspiron Intel 27 7700 11th Generation Core I7-1165G7 16GB RAM, 1TB HDD+512GB SSD.\r\n', 'dell', 'static/uploads\\dellc7.jpg'),
(72, 'Desktop', 'ASUS', 43000, '1', 'ASUS A3402, 23.8\" FHD, 13th Gen, Intel Core i3-1315U, 8GB RAM/512GB SSD.', 'asus', 'static/uploads\\asusc1.jpg'),
(73, 'Desktop', 'ASUS', 56000, '1', 'ASUS AiO M3 Series, 27\" FHD, AMD Ryzen 5 7520U, Desktop 16GB/512GB SSD.', 'asus', 'static/uploads\\asusc2.jpg'),
(74, 'Desktop', 'ASUS', 63000, '1', 'ASUS AiO A3 Series, 23.8\" FHD, Intel Core i5-1235U 12th Gen, Desktop 8GB/512GB SSD.', 'asus', 'static/uploads\\asusc3.jpg'),
(75, 'Desktop', 'ASUS', 64000, '1', 'ASUS A3402, 23.8\" FHD, 13th Gen, Intel Core i5-1335U, (16GB RAM/1TB SSD.', 'asus', 'static/uploads\\asusc4.jpg'),
(76, 'Desktop', 'ASUS', 54000, '1', 'ASUS A3402, 23.8\" FHD, 13th Gen, Intel Core i5-1335U, 8GB RAM/512GB SSD.', 'asus', 'static/uploads\\asusc5.jpg'),
(77, 'Desktop', 'ASUS', 49000, '1', 'ASUS A3402, 23.8\", Intel Core i3-1315U, Desktop 8GB RAM/512GB SSD.', 'asus', 'static/uploads\\asusc6.jpg'),
(79, 'Desktop', 'ASUS', 63000, '1', 'ASUS AiO A3 Series, 23.8\" FHD, Intel Core i5-1235U 12th Gen, 8GB/512GB SSD.', 'asus', 'static/uploads\\asusc7.jpg'),
(80, 'Desktop', 'ASUS', 30000, '1', 'ASUS Vivo AiO V222, 4 core Intel Pentium Silver J5040, 8GB/256GB SSD.', 'asus', 'static/uploads\\asusc8.jpg'),
(81, 'Desktop', 'APPLE', 130000, '1', 'iMac 8-core GPU: Built for Apple Intelligence, (24″) Retina Display, 16GB, 256GB SSD.', 'apple', 'static/uploads\\applec.jpg'),
(82, 'Desktop', 'APPLE', 150000, '1', 'iMac with M4 chip with 10-core CPU Retina Display, 16GB Memory, 256GB SSD Storage.', 'apple', 'static/uploads\\applec2.jpg'),
(88, 'Desktop', 'APPLE', 134000, '1', 'iMac 60.96 cm (24″) Retina Display, 16GB Memory, 256GB SSD Storage.', 'apple', 'static/uploads\\applec6.jpg'),
(90, 'Desktop', 'APPLE', 154000, '1', 'iMac (24-inch, Apple M3 chip 8GB Memory, 512GB Storage.', 'apple', 'static/uploads\\applec7.jpg'),
(91, 'Desktop', 'APPLE', 170000, '1', ' iMac (24-inch, M3 chip with 8‑core CPU and 10‑core GPU, 16GB Memory, 512GB.', 'apple', 'static/uploads\\applec.jpg'),
(92, 'Desktop', 'APPLE', 170000, '1', 'iMac with M4 chip with 10-core CPU Retina Display, 16GB Memory, 512GB SSD Storage.', 'apple', 'static/uploads\\applec2.jpg'),
(93, 'Desktop', 'APPLE', 135000, '1', 'iMac with M4 chip with 60.96 cm (24″) Retina Display, 16GB Memory, 256GB SSD Storage.', 'apple', 'static/uploads\\applec3.jpg'),
(94, 'Desktop', 'APPLE', 139000, '1', 'iMac (24-inch, Apple M3 chip with 8‑core CPU and 10‑core GPU, 8GB Memory, 256GB.', 'apple', 'static/uploads\\applec4.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_adminlog`
--

CREATE TABLE `tbl_adminlog` (
  `id` int(9) NOT NULL,
  `email` int(100) NOT NULL,
  `password` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_adminlog`
--

INSERT INTO `tbl_adminlog` (`id`, `email`, `password`) VALUES
(1, 0, 0),
(2, 0, 123),
(3, 0, 111),
(4, 0, 123),
(5, 0, 1212);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_adminsign`
--

CREATE TABLE `tbl_adminsign` (
  `id` int(9) NOT NULL,
  `full_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone_number` bigint(10) NOT NULL,
  `password` varchar(20) NOT NULL,
  `confirm_password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_adminsign`
--

INSERT INTO `tbl_adminsign` (`id`, `full_name`, `email`, `phone_number`, `password`, `confirm_password`) VALUES
(1, 'Sarthak ', 'sp@gmail.com', 0, '1212', '1212'),
(2, 'Prathmesh ', 'patilprathm2003@gmail.com', 0, '1234', '1234'),
(3, 'Prathmesh', 'patilprathm2003@gmail.com', 8605843620, '1234', '1234'),
(4, 'Prathmesh', 'patilprathm2003@gmail.com', 8605843620, '1234', '1234'),
(5, 'Prathmesh', 'patilprathm2003@gmail.com', 8605843620, '1234', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_booking`
--

CREATE TABLE `tbl_booking` (
  `id` int(9) NOT NULL,
  `user_id` int(9) NOT NULL,
  `full_name` varchar(50) NOT NULL,
  `email_address` varchar(100) NOT NULL,
  `contact_number` bigint(10) NOT NULL,
  `enter_product` varchar(20) NOT NULL,
  `price` varchar(200) NOT NULL,
  `quantity` int(100) NOT NULL,
  `total_amount` varchar(100) NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_booking`
--

INSERT INTO `tbl_booking` (`id`, `user_id`, `full_name`, `email_address`, `contact_number`, `enter_product`, `price`, `quantity`, `total_amount`, `status`) VALUES
(37, 10, 'Prathmesh', 'patilprathm2003@gmail.com', 8605843620, 'ASUS, ROG Strix G17 ', '₹88000.0', 1, '88000.00', 'Confirm'),
(38, 11, 'Samrudhi Patil', 'samrudhi@gmail.com', 7218951686, 'APPLE, MacBook Pro (', '₹349000.0', 2, '698000.00', 'Delivered'),
(39, 12, 'Siddhivinayak Darekar', 'sid@gmail.com', 90245566909, 'DELL, Gaming 13th Ge', '₹116000.0', 3, '348000.00', 'In Process'),
(40, 10, 'Prathmesh', 'patilprathm2003@gmail.com', 8605843620, 'HP, 13th Gen Intel C', '₹70000.0', 1, '70000.00', 'Canceled'),
(41, 10, 'Prathmesh', 'patilprathm2003@gmail.com', 8605843620, 'HP, 13th Gen Intel C', '₹70000.0', 2, '140000.00', 'In Process'),
(42, 10, 'Prathmesh', 'patilprathm2003@gmail.com', 8605843620, 'HP, HP Desktop 24 PC', '₹60000.0', 1, '60000.00', 'In Process'),
(43, 11, 'Samrudhi Patil', 'samrudhi@gmail.com', 7218951686, 'HP, 13th Gen Intel C', '₹70000.0', 1, '70000.00', 'Delivered'),
(44, 12, 'Siddhivinayak Darekar', 'sid@gmail.com', 90245566909, 'ASUS, ASUS A3402, 23', '₹49000.0', 3, '147000.00', 'In Process'),
(45, 12, 'Siddhivinayak Darekar', 'sid@gmail.com', 90245566909, 'ASUS, ASUS A3402, 23', '₹49000.0', 2, '98000.00', 'Delivered'),
(46, 12, 'Siddhivinayak Darekar', 'sid@gmail.com', 90245566909, 'ASUS, ASUS A3402, 23', '₹49000.0', 1, '49000.00', 'Delivered'),
(47, 12, 'Siddhivinayak Darekar', 'sid@gmail.com', 90245566909, 'ASUS, ASUS A3402, 23', '₹49000.0', 2, '98000.00', 'Canceled'),
(48, 12, 'Siddhivinayak Darekar', 'sid@gmail.com', 90245566909, 'ASUS, ASUS A3402, 23', '₹49000.0', 1, '49000.00', 'Confirm'),
(49, 12, 'Siddhivinayak Darekar', 'sid@gmail.com', 90245566909, 'DELL, 5520 Gaming La', '₹76000.0', 1, '76000.00', 'In Process'),
(50, 11, 'Samrudhi Patil', 'samrudhi@gmail.com', 7218951686, 'DELL, 7420 2in1 Lapt', '₹86000.0', 2, '172000.00', 'In Process'),
(51, 10, 'Prathmesh', 'patilprathm2003@gmail.com', 8605843620, 'HP, Gaming Laptop 12', '₹66000.0', 4, '264000.00', ''),
(52, 11, 'Samrudhi Patil', 'samrudhi@gmail.com', 7218951686, 'ASUS, ASUS A3402, 23', '₹54000.0', 3, '162000.00', 'In Process'),
(53, 12, 'Siddhivinayak Darekar', 'sid@gmail.com', 90245566909, 'APPLE, Laptop 14.2-i', '₹187000.0', 4, '748000.00', 'Canceled'),
(54, 11, 'Samrudhi Patil', 'samrudhi@gmail.com', 7218951686, 'HP, 13th Gen Intel C', '₹61000.0', 2, '122000.00', ''),
(55, 11, 'Samrudhi Patil', 'samrudhi@gmail.com', 7218951686, 'DELL, 5520 Gaming La', '₹76000.0', 1, '76000.00', ''),
(56, 11, 'Samrudhi Patil', 'samrudhi@gmail.com', 7218951686, 'DELL, 5520 Gaming La', '₹76000.0', 2, '152000.00', ''),
(57, 11, 'Samrudhi Patil', 'samrudhi@gmail.com', 7218951686, 'DELL, 5520 Gaming La', '₹76000.0', 3, '228000.00', ''),
(58, 11, 'Samrudhi Patil', 'samrudhi@gmail.com', 7218951686, 'DELL, 5520 Gaming La', '₹76000.0', 2, '152000.00', ''),
(59, 11, 'Samrudhi Patil', 'samrudhi@gmail.com', 7218951686, 'DELL, 5520 Gaming La', '₹76000.0', 1, '76000.00', '');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_cd`
--

CREATE TABLE `tbl_cd` (
  `id` int(9) NOT NULL,
  `name` varchar(20) NOT NULL,
  `card_number` varchar(20) NOT NULL,
  `expiry_date` varchar(20) NOT NULL,
  `cvv` varchar(20) NOT NULL,
  `total_amount` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_cd`
--

INSERT INTO `tbl_cd` (`id`, `name`, `card_number`, `expiry_date`, `cvv`, `total_amount`) VALUES
(1, 'Prathmesh Mahesh Pat', '5432123456789101', '2002-02-12', '121', '748000.00'),
(2, 'Samrudhi Patil', '5432123456789101', '2012-02-12', '121', '76000.00');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_complaint`
--

CREATE TABLE `tbl_complaint` (
  `id` int(9) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `number` bigint(10) NOT NULL,
  `complaint_type` varchar(20) NOT NULL,
  `complaint_descrip` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_complaint`
--

INSERT INTO `tbl_complaint` (`id`, `first_name`, `last_name`, `email`, `number`, `complaint_type`, `complaint_descrip`) VALUES
(1, 'Vaidehi ', 'Patil', 'vd@gmail.com', 7218951680, 'Software Issue', 'hi');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_feedback`
--

CREATE TABLE `tbl_feedback` (
  `id` int(9) NOT NULL,
  `full_name` varchar(50) NOT NULL,
  `email_address` varchar(100) NOT NULL,
  `rating` varchar(50) NOT NULL,
  `your_feedback` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_feedback`
--

INSERT INTO `tbl_feedback` (`id`, `full_name`, `email_address`, `rating`, `your_feedback`) VALUES
(1, 'Prathmesh Mahesh Patil', 'patilprathm2003@gmail.com', 'excellent', 'helloji'),
(2, 'Prathm Patil', 'patilprathm2003@gmail.com', 'good', 'Nice');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_upi`
--

CREATE TABLE `tbl_upi` (
  `id` int(9) NOT NULL,
  `full_name` varchar(50) NOT NULL,
  `email_address` varchar(100) NOT NULL,
  `phone_number` bigint(10) NOT NULL,
  `upi_id` varchar(20) NOT NULL,
  `amount` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_upi`
--

INSERT INTO `tbl_upi` (`id`, `full_name`, `email_address`, `phone_number`, `upi_id`, `amount`) VALUES
(1, 'Prathmesh Mahesh Patil', 'patilprathm2003@gmail.com', 8605843620, '988776655', 0),
(2, 'Prathmesh Mahesh Patil', 'patilprathm2003@gmail.com', 8605843620, '988776655', 0),
(3, 'Samrudhi Patil', 'samrudhi@gmail.com', 7218951686, '988776655', 176000),
(4, 'Samrudhi Patil', 'samrudhi@gmail.com', 7218951686, '988776655', 176000),
(5, 'Siddhivinayak Darekar', 'sid@gmail.com', 9024556690, '1234567890', 76000),
(6, 'Samrudhi Patil', 'samrudhi@gmail.com', 7218951686, '1234567890', 172000),
(7, 'Samrudhi Patil', 'samrudhi@gmail.com', 7218951686, '1234567890', 172000),
(8, 'Prathmesh Mahesh Patil', 'patilprathm2003@gmail.com', 8605843620, '1234567890', 264000),
(9, 'Samrudhi Patil', 'samrudhi@gmail.com', 7218951686, '1234567890', 162000);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_userlog`
--

CREATE TABLE `tbl_userlog` (
  `id` int(9) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_usersign`
--

CREATE TABLE `tbl_usersign` (
  `id` int(9) NOT NULL,
  `full_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone_number` bigint(10) NOT NULL,
  `password` varchar(50) NOT NULL,
  `confirm_password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_usersign`
--

INSERT INTO `tbl_usersign` (`id`, `full_name`, `email`, `phone_number`, `password`, `confirm_password`) VALUES
(10, 'Prathmesh', 'patilprathm2003@gmail.com', 8605843620, '1111', '1111'),
(11, 'Samrudhi Patil', 'samrudhi@gmail.com', 7218951686, '1212', '1212'),
(12, 'Siddhivinayak Darekar', 'sid@gmail.com', 90245566909, '1234', '1234');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_addcategory`
--
ALTER TABLE `tbl_addcategory`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_addproduct`
--
ALTER TABLE `tbl_addproduct`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_adminlog`
--
ALTER TABLE `tbl_adminlog`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_adminsign`
--
ALTER TABLE `tbl_adminsign`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_booking`
--
ALTER TABLE `tbl_booking`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_cd`
--
ALTER TABLE `tbl_cd`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_complaint`
--
ALTER TABLE `tbl_complaint`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_feedback`
--
ALTER TABLE `tbl_feedback`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_upi`
--
ALTER TABLE `tbl_upi`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_userlog`
--
ALTER TABLE `tbl_userlog`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_usersign`
--
ALTER TABLE `tbl_usersign`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_addcategory`
--
ALTER TABLE `tbl_addcategory`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `tbl_addproduct`
--
ALTER TABLE `tbl_addproduct`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=95;

--
-- AUTO_INCREMENT for table `tbl_adminlog`
--
ALTER TABLE `tbl_adminlog`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `tbl_adminsign`
--
ALTER TABLE `tbl_adminsign`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `tbl_booking`
--
ALTER TABLE `tbl_booking`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

--
-- AUTO_INCREMENT for table `tbl_cd`
--
ALTER TABLE `tbl_cd`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `tbl_complaint`
--
ALTER TABLE `tbl_complaint`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `tbl_feedback`
--
ALTER TABLE `tbl_feedback`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tbl_upi`
--
ALTER TABLE `tbl_upi`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `tbl_userlog`
--
ALTER TABLE `tbl_userlog`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `tbl_usersign`
--
ALTER TABLE `tbl_usersign`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
