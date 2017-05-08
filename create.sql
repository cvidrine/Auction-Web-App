drop table if exists Items;
drop table if exists Users;
drop table if exists Categories;
drop table if exists Bids;
drop table if exists CurrentTime;
create table Users(UserID TEXT PRIMARY KEY, Rating INTEGER, Location TEXT, Country TEXT);
create table Items(ItemID TEXT PRIMARY KEY, UserID TEXT REFERENCES Users(UserID), Name TEXT, Buy_Price REAL, First_Bid REAL, Currently REAL, 
    Number_of_Bids INTEGER, Started TEXT, Ends TEXT check(Ends>Started), Description TEXT);
create table Categories(ItemID TEXT REFERENCES Items(ItemID), Category TEXT, UNIQUE(ItemID, Category));
create table Bids(ItemID TEXT REFERENCES Items(ItemID), UserID TEXT REFERENCES Users(UserID), Time TEXT, Amount REAL, UNIQUE(ItemID, Time), UNIQUE(ItemID, UserID, Amount));
create table CurrentTime(CurrentTime TEXT);
insert into CurrentTime values ("2001-12-20 00:00:01");
select * from CurrentTime;
