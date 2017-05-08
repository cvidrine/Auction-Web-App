 --Description: Ensures that the current time can only advance 
PRAGMA foreign_keys = ON;
drop trigger if exists current_time_change;
create trigger current_time_change
before insert on CurrentTime
for each row
when exists(
    select *
    from CurrentTime
    where CurrentTime >= new.CurrentTime
)
begin
    select raise(rollback, "Current time can not be changed to a time in the past.");
end;

  --Description: Ensures that the CurrentTime table always has only one tuple. 
PRAGMA foreign_keys = ON;
drop trigger if exists clear_timetable;
create trigger clear_timetable
before insert on CurrentTime
for each row
begin
    delete from CurrentTime where CurrentTime < new.CurrentTime;    
end;


