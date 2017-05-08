--Description: Ensures that no bids happen before an auctions start time or after its end time.
PRAGMA foreign_keys = ON;
drop trigger if exists bid_timer;
create trigger bid_timer
after insert on Bids
for each row
when exists (
    Select *
    from Items
    where ItemID = new.ItemID AND (Started > new.Time OR Ends < new.Time))
begin
    select raise(rollback, "Bids must occur after an auction's start time or before their end time.");
end;    

