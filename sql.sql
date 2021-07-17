create table village_details(
vill_name varchar(100) not null primary key,
vill_area smallint not null,
vill_population smallint not null,
vill_cattle_population smallint ,
vill_sheep_population smallint ,
vill_poultry_population smallint);

insert into village_details values('Sinnar_konambe', 2022, 3113, 3000, 700, 20000);
insert into village_details values('Shirur_kanhur', 2633, 4028, 3000, 700, 20000);

create table crop_kharif_details(
vill_name varchar(100) references village_details(vill_name),
crop_name varchar(100) not null,
crop_area smallint not null,
crop_sowdate varchar(10) not null,
crop_area_drip smallint,
crop_apmc_market varchar(50) not null);

#Konambe
insert into crop_kharif_details values('Sinnar_konambe','Carrot',360,'01-06-2020',0,'Sinnar');
insert into crop_kharif_details values('Sinnar_konambe','Soyabean',420,'01-06-2020',0,'Sinnar');
insert into crop_kharif_details values('Sinnar_konambe','Tomato',180,'01-06-2020',0,'Sinnar');
insert into crop_kharif_details values('Sinnar_konambe','Groundnut',20,'01-06-2020',0,'Sinnar');
insert into crop_kharif_details values('Sinnar_konambe','Lentil',20,'01-06-2020',0,'Sinnar');
insert into crop_kharif_details values('Sinnar_konambe','Pea',20,'01-06-2020',0,'Sinnar');
insert into crop_kharif_details values('Sinnar_konambe','Cabbage',120,'01-06-2020',0,'Sinnar');

#KanhurMesai
insert into crop_kharif_details values('Shirur_kanhur','Lentil',432,'15-06-2020',0,'Pune');
insert into crop_kharif_details values('Shirur_kanhur','Millet',1242,'15-06-2020',0,'Pune');
insert into crop_kharif_details values('Shirur_kanhur','Onion-dry',312,'01-08-2020',0,'Pune');
insert into crop_kharif_details values('Shirur_kanhur','Bean-green',85,'15-06-2020',0,'Pune');
insert into crop_kharif_details values('Shirur_kanhur','Tomato',14,'15-06-2020',0,'Pune');


create table crop_rabi_details(
vill_name varchar(100) references village_details(vill_name),
crop_name varchar(100) not null,
crop_area smallint not null,
crop_sowdate varchar(10) not null,
crop_area_drip smallint,
crop_apmc_market varchar(50) not null);

#Konambe
insert into crop_rabi_details values('Sinnar_konambe','Wheat',135,'01-11-2020',0,'Sinnar');
insert into crop_rabi_details values('Sinnar_konambe','Onion-dry',360,'01-11-2020',10,'Sinnar');
insert into crop_rabi_details values('Sinnar_konambe','Tomato',180,'01-08-2020',90,'Sinnar');
insert into crop_rabi_details values('Sinnar_konambe','Carrot'45,,'01-11-2020',40,'Sinnar');
insert into crop_rabi_details values('Sinnar_konambe','Millet',45,'01-11-2020',0,'Sinnar');
insert into crop_rabi_details values('Sinnar_konambe','Maize-grain',27,'01-11-2020',0,'Sinnar');
insert into crop_rabi_details values('Sinnar_konambe','Cabbage',63,'01-11-2020',20,'Sinnar');

#KanhurMesai
insert into crop_rabi_details values('Shirur_kanhur','Onion-dry',472,'01-10-2020',0,'Pune');
insert into crop_rabi_details values('Shirur_kanhur','Sorghum',742,'01-10-2020',0,'Pune');
insert into crop_rabi_details values('Shirur_kanhur','Tomato',90,'15-10-2020',0,'Pune');