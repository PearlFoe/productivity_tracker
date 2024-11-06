INSERT INTO pt.calendar_category (id, name) 
VALUES (
    'b2770739-2659-4409-a02e-619dfb2a64fa'::uuid, 
    'work'
) 
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;

INSERT INTO pt.calendar_category (id, name) 
VALUES (
    '157db555-b115-41e7-a50e-354b9f601e10'::uuid, 
    'entertainment'
) 
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;