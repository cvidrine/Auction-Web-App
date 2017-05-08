-- Description: Updates Number_Of_Bids when a new bid is made.
PRAGMA foreign_keys = ON;
drop trigger if exists update_numbids;
create trigger update_numbids
after insert on Bids
for each row
begin
    update Items set Number_Of_Bids = Number_Of_Bids + 1 where
    ItemID = new.ItemID;
end;    
