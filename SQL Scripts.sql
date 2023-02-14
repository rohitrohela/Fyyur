-- VENUE TABLE --

insert into public."Venue"(id, name, city, state, address, phone, image_link, facebook_link)
values(1, 'The Musical Hop', 'San Francisco', 'CA', '1015 Folsom Street', '1231231234',
	   'https://images.unsplash.com/photo-1543900694-133f3…hcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60','https://www.facebook.com/TheMusicalHop');

insert into public."Venue"(id, name, city, state, address, phone, image_link, facebook_link)
values(2, 'The Dueling Pianos Bar', 'New York', 'NY', '335 Delancey Street', '9140031132',
	   'https://images.unsplash.com/photo-1497032205916-ac…hcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80','https://www.facebook.com/theduelingpianos');

insert into public."Venue"(id, name, city, state, address, phone, image_link, facebook_link)
values(3, 'Park Square Live Music & Coffee', 'San Francisco', 'CA', '34 Whiskey Moore Ave', '415000234',
	   'https://images.unsplash.com/photo-1485686531765-ba…hcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80','https://www.facebook.com/ParkSquareLiveMusicAndCoffee');
	   
--Artist table--

insert into public."Artist"(id,name, city, state, phone, genres, image_link, facebook_link, website_link)
values(4, 'GUNS N PETALS', 'CA', 'San Francisco', '3261235000', 'Rock n Roll', 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
	  'https://www.gunsnpetalsband.com','https://www.facebook.com/GunsNPetals');

insert into public."Artist"(id,name, city, state, phone, genres, image_link, facebook_link, website_link)
values(5, 'MATT QUEVEDO', 'NY', 'New York', '3261235000', 'Jazz', '	https://images.unsplash.com/photo-1495223153807-b9…hcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
	  'https://www.facebook.com/mattquevedo923251523', null);

insert into public."Artist"(id,name, city, state, phone, genres, image_link, facebook_link, website_link)
values(6, 'THE WILD SAX BAND', 'CA', 'San Francisco', '3261235000', 'Jazz, Classical', 'https://images.unsplash.com/photo-1558369981-f9ca7…hcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
	  null, null);
