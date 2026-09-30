DROP TABLE IF EXISTS stores;

CREATE TABLE stores (
    store_id INTEGER PRIMARY KEY,
    store_name TEXT NOT NULL UNIQUE,
    city TEXT NOT NULL,
    region TEXT NOT NULL,
    opening_date TEXT NOT NULL
);

INSERT INTO stores (store_id, store_name, city, region, opening_date) VALUES
(1, 'FreshWave Paris République', 'Paris', 'Île-de-France', '2022-04-10'),
(2, 'FreshWave Paris Montparnasse', 'Paris', 'Île-de-France', '2022-06-15'),
(3, 'FreshWave Paris Bastille', 'Paris', 'Île-de-France', '2023-02-01'),
(4, 'FreshWave Lyon Part-Dieu', 'Lyon', 'Auvergne-Rhône-Alpes', '2022-05-10'),
(5, 'FreshWave Lyon Bellecour', 'Lyon', 'Auvergne-Rhône-Alpes', '2023-01-15'),
(6, 'FreshWave Marseille Vieux-Port', 'Marseille', 'Provence-Alpes-Côte d''Azur', '2022-07-01'),
(7, 'FreshWave Marseille Prado', 'Marseille', 'Provence-Alpes-Côte d''Azur', '2023-03-20'),
(8, 'FreshWave Bordeaux Centre', 'Bordeaux', 'Nouvelle-Aquitaine', '2022-04-22'),
(9, 'FreshWave Lille Grand Place', 'Lille', 'Hauts-de-France', '2022-09-15'),
(10, 'FreshWave Nantes Commerce', 'Nantes', 'Pays de la Loire', '2023-04-01'),
(11, 'FreshWave Toulouse Capitole', 'Toulouse', 'Occitanie', '2022-06-30'),
(12, 'FreshWave Nice Promenade', 'Nice', 'Provence-Alpes-Côte d''Azur', '2023-05-15');
