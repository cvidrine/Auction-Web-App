-- description: Updates Currently in Items table when a bid is made for an item.
PRAGMA foreign_keys = ON;
drop trigger if exists update_currently;
create trigger update_currently
after insert on Bids
for each row
begin
    update Items set Currently = new.Amount where
    ItemID = new.ItemID;
end;    
