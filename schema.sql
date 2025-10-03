
CREATE TABLE authors (
	au_id VARCHAR(11) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	au_lname VARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	au_fname VARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	phone CHAR(12) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL DEFAULT ('UNKNOWN'), 
	address VARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	city VARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	state CHAR(2) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	zip CHAR(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	contract BIT NOT NULL, 
	CONSTRAINT [UPKCL_auidind] PRIMARY KEY CLUSTERED (au_id)
)


CREATE NONCLUSTERED INDEX aunmind ON authors (au_lname, au_fname)

CREATE TABLE stores (
	stor_id CHAR(4) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	stor_name VARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	stor_address VARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	city VARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	state CHAR(2) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	zip CHAR(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	CONSTRAINT [UPK_storeid] PRIMARY KEY CLUSTERED (stor_id)
)



CREATE TABLE jobs (
	job_id SMALLINT NOT NULL IDENTITY(1,1), 
	job_desc VARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL DEFAULT ('New Position - title not formalized yet'), 
	min_lvl TINYINT NOT NULL, 
	max_lvl TINYINT NOT NULL, 
	CONSTRAINT [PK__jobs__6E32B6A5263A94A2] PRIMARY KEY CLUSTERED (job_id)
)



CREATE TABLE publishers (
	pub_id CHAR(4) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	pub_name VARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	city VARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	state CHAR(2) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	country VARCHAR(30) COLLATE SQL_Latin1_General_CP1_CI_AS NULL DEFAULT ('USA'), 
	CONSTRAINT [UPKCL_pubind] PRIMARY KEY CLUSTERED (pub_id)
)



CREATE TABLE titleview (
	title VARCHAR(80) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	au_ord TINYINT NULL, 
	au_lname VARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	price MONEY NULL, 
	ytd_sales INTEGER NULL, 
	pub_id CHAR(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
)



CREATE TABLE discounts (
	discounttype VARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	stor_id CHAR(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	lowqty SMALLINT NULL, 
	highqty SMALLINT NULL, 
	discount DECIMAL(4, 2) NOT NULL, 
	CONSTRAINT [FK__discounts__stor___4F7CD00D] FOREIGN KEY(stor_id) REFERENCES stores (stor_id)
)



CREATE TABLE employee (
	emp_id VARCHAR(9) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	fname VARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	minit CHAR(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	lname VARCHAR(30) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	job_id SMALLINT NOT NULL DEFAULT ((1)), 
	job_lvl TINYINT NULL DEFAULT ((10)), 
	pub_id CHAR(4) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL DEFAULT ('9952'), 
	hire_date DATETIME NOT NULL DEFAULT (getdate()), 
	CONSTRAINT [PK_emp_id] PRIMARY KEY NONCLUSTERED (emp_id), 
	CONSTRAINT [FK__employee__job_id__5BE2A6F2] FOREIGN KEY(job_id) REFERENCES jobs (job_id), 
	CONSTRAINT [FK__employee__pub_id__5EBF139D] FOREIGN KEY(pub_id) REFERENCES publishers (pub_id)
)


CREATE CLUSTERED INDEX employee_ind ON employee (fname, minit, lname)

CREATE TABLE pub_info (
	pub_id CHAR(4) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	logo IMAGE NULL, 
	pr_info TEXT(16) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	CONSTRAINT [UPKCL_pubinfo] PRIMARY KEY CLUSTERED (pub_id), 
	CONSTRAINT [FK__pub_info__pub_id__571DF1D5] FOREIGN KEY(pub_id) REFERENCES publishers (pub_id)
)



CREATE TABLE titles (
	title_id VARCHAR(6) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	title VARCHAR(80) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	type CHAR(12) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL DEFAULT ('UNDECIDED'), 
	pub_id CHAR(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	price MONEY NULL, 
	advance MONEY NULL, 
	royalty INTEGER NULL, 
	ytd_sales INTEGER NULL, 
	notes VARCHAR(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	pubdate DATETIME NOT NULL DEFAULT (getdate()), 
	CONSTRAINT [UPKCL_titleidind] PRIMARY KEY CLUSTERED (title_id), 
	CONSTRAINT [FK__titles__pub_id__412EB0B6] FOREIGN KEY(pub_id) REFERENCES publishers (pub_id)
)


CREATE NONCLUSTERED INDEX titleind ON titles (title)

CREATE TABLE roysched (
	title_id VARCHAR(6) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	lorange INTEGER NULL, 
	hirange INTEGER NULL, 
	royalty INTEGER NULL, 
	CONSTRAINT [FK__roysched__title___4D94879B] FOREIGN KEY(title_id) REFERENCES titles (title_id)
)


CREATE NONCLUSTERED INDEX titleidind ON roysched (title_id)

CREATE TABLE sales (
	stor_id CHAR(4) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	ord_num VARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	ord_date DATETIME NOT NULL, 
	qty SMALLINT NOT NULL, 
	payterms VARCHAR(12) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	title_id VARCHAR(6) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	CONSTRAINT [UPKCL_sales] PRIMARY KEY CLUSTERED (stor_id, ord_num, title_id), 
	CONSTRAINT [FK__sales__stor_id__4AB81AF0] FOREIGN KEY(stor_id) REFERENCES stores (stor_id), 
	CONSTRAINT [FK__sales__title_id__4BAC3F29] FOREIGN KEY(title_id) REFERENCES titles (title_id)
)


CREATE NONCLUSTERED INDEX titleidind ON sales (title_id)

CREATE TABLE titleauthor (
	au_id VARCHAR(11) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	title_id VARCHAR(6) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	au_ord TINYINT NULL, 
	royaltyper INTEGER NULL, 
	CONSTRAINT [UPKCL_taind] PRIMARY KEY CLUSTERED (au_id, title_id), 
	CONSTRAINT [FK__titleauth__au_id__44FF419A] FOREIGN KEY(au_id) REFERENCES authors (au_id), 
	CONSTRAINT [FK__titleauth__title__45F365D3] FOREIGN KEY(title_id) REFERENCES titles (title_id)
)


CREATE NONCLUSTERED INDEX titleidind ON titleauthor (title_id)
CREATE NONCLUSTERED INDEX auidind ON titleauthor (au_id)
