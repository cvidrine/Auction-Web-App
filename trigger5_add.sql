--Description: Ensures that any new bid is higher than the previous bid. 
PRAGMA foreign_keys = ON;
drop trigger if exists highest_bid;
create trigger highest_bid
before insert on Bids
for each row
when exists (
    Select *
    from Bids
    where ItemID = new.ItemID and Amount >= new.Amount)
begin
    select raise(rollback, "New bids must be higher than the current highest bid.");
end;    
