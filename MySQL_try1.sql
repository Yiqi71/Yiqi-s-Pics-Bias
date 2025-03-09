alter table pictures
-- add familiar varchar(100);
modify familiar varchar(100)
after pic_src;
    
select * from pictures
