-- description: Ensures that a user does not bid on an item that they are currently selling.
PRAGMA foreign_keys = ON;
drop trigger if exists seller_not_buyer;
create trigger seller_not_buyer
after insert on Bids
for each row
when exists (
    Select *
    from Items
    where ItemID = new.ItemID and UserID = new.UserID
)
begin
    select raise(rollback, "A seller can not bid on an item that they are selling.");
end;    
