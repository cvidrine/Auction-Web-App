select * from Bids where UserID NOT IN (select userID from Users);
select * from Items where UserID NOT IN (select userID from Users);
select * from Bids where ItemID NOT IN (select ItemID from Items);
select * from Categories where ItemID NOT IN (select ItemID from Items);
