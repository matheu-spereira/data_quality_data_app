Create SCHEMA sistema
CREATE TABLE sistema.pessoas (
    id SERIAL PRIMARY KEY NOT NULL,
    nome TEXT ,
    idade INT,
    cpf TEXT,
    data_nascimento DATE
);

INSERT INTO sistema.pessoas (nome, idade, cpf, data_nascimento) VALUES
('Ana', 30, '123.456.789-00', '1993-01-15'),
('Bruno', NULL, NULL, NULL),
('Carlos', 30, '987.654.321-00', '1993-01-15'),
('Ana', 30, '123.456.789-00', '1993-01-15'), -- duplicado
('Daniela', 28, '111.111.111-11', '1995-04-10'),
('Eduardo', 35, NULL, '1988-07-25'),
('Fernanda', NULL, NULL, NULL),
('Gabriel', 40, '222.222.222-22', '1983-12-01'),
('Helena', 22, '333.333.333-33', NULL),
('Igor', NULL, '444.444.444-44', '1990-10-10'),
('Juliana', 30, '555.555.555-55', '1993-01-15'),
('Carlos', 30, '987.654.321-00', '1993-01-15'), -- duplicado
('Lucas', NULL, NULL, NULL),
('Mariana', 29, '666.666.666-66', '1994-03-03'),
('Nicolas', 27, NULL, NULL),
('Olivia', 31, '777.777.777-77', '1992-06-06'),
('Pedro', 30, '888.888.888-88', NULL),
('Quintino', 33, NULL, '1990-11-11'),
('Rafaela', NULL, NULL, NULL),
('Samuel', 36, '999.999.999-99', '1987-09-09'),
('Tatiane', 28, '000.000.000-00', '1995-02-02');

COMMENT ON COLUMN sistema.pessoas.id IS 'Identificador único da pessoa.';
COMMENT ON COLUMN sistema.pessoas.nome IS 'Nome completo da pessoa.';
COMMENT ON COLUMN sistema.pessoas.idade IS 'Idade declarada da pessoa.';
COMMENT ON COLUMN sistema.pessoas.cpf IS 'CPF no formato 000.000.000-00.';
COMMENT ON COLUMN sistema.pessoas.data_nascimento IS 'Data de nascimento da pessoa.';

CREATE TABLE sistema.enderecos (
    id SERIAL PRIMARY KEY NOT NULL,
    pessoa_id INT  NOT NULL,
    rua TEXT,
    numero TEXT,
    cidade TEXT,
    estado TEXT,
    cep TEXT
);

INSERT INTO sistema.enderecos (pessoa_id, rua, numero, cidade, estado, cep) VALUES
(1, 'Rua das Flores', '123', 'São Paulo', 'SP', '01000-000'),
(3, 'Av. Brasil', '456', 'Rio de Janeiro', '', '20000-000'),
(5, 'Rua Central', '', 'Belo Horizonte', 'MG', '30000-000'),
(7, 'Av. Paulista', '1001', 'São Paulo', 'SP', ''),
(8, 'Rua dos Andradas', '', 'Porto Alegre', 'RS', '90020-005');

COMMENT ON TABLE sistema.enderecos IS 'Endereços residenciais associados às pessoas.';
COMMENT ON COLUMN sistema.enderecos.id IS 'Identificador único do endereço.';
COMMENT ON COLUMN sistema.enderecos.pessoa_id IS 'Chave estrangeira que referencia a pessoa.';
COMMENT ON COLUMN sistema.enderecos.rua IS 'Nome da rua.';
COMMENT ON COLUMN sistema.enderecos.numero IS 'Número da residência (complementos possíveis).';
COMMENT ON COLUMN sistema.enderecos.cidade IS 'Cidade do endereço.';
COMMENT ON COLUMN sistema.enderecos.estado IS 'UF (estado) do endereço.';
COMMENT ON COLUMN sistema.enderecos.cep IS 'CEP no formato 00000-000.';



CREATE SCHEMA site

CREATE TABLE site.acessos (
    id SERIAL PRIMARY KEY NOT NULL ,
    pessoa_id INT  NOT NULL,
    data_acesso TIMESTAMP,
    acao TEXT  -- Ex: 'login', 'logout', 'consulta_dados'
);

INSERT INTO site.acessos (pessoa_id, data_acesso, acao) VALUES
(1, '2024-12-01 09:15:00', 'login'),
(1, '2024-12-01 10:00:00', 'consulta_dados'),
(3, '2024-12-02 11:20:00', 'login'),
(3, '2024-12-02 12:00:00', 'logout'),
(5, '2024-12-03 08:45:00', 'login'),
(8, '2024-12-04 14:10:00', 'consulta_dados'),
(11, '2024-12-05 16:00:00', 'login'),
(11, '2024-12-05 16:30:00', 'consulta_dados'),
(11, '2024-12-05 17:00:00', 'logout');
