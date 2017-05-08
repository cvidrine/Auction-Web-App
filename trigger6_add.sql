--Description: Ensures that any new bid happens at the Current Time 
PRAGMA foreign_keys = ON;
drop trigger if exists bid_current_time;
create trigger bid_current_time
before insert on Bids
for each row
when exists (
    Select *
    from CurrentTime
    where CurrentTime != new.Time)
begin
    select raise(rollback, "Bids must occur at the current System time.");
end;    
