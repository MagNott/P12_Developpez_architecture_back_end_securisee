--
-- PostgreSQL database dump
--

\restrict 6PSsmRken6ghKLNAlu4bALehcmMyPa4AweFwFSpkvysEqRhYbH8PVszvEJyc1Qv

-- Dumped from database version 14.19 (Ubuntu 14.19-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 17.6

-- Started on 2025-10-31 13:49:24

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3358 (class 0 OID 24577)
-- Dependencies: 210
-- Data for Name: departments; Type: TABLE DATA; Schema: public; Owner: p12_user
--

INSERT INTO public.departments VALUES (3, 'Support');
INSERT INTO public.departments VALUES (1, 'Sales');
INSERT INTO public.departments VALUES (2, 'Management');


--
-- TOC entry 3362 (class 0 OID 24595)
-- Dependencies: 214
-- Data for Name: collaborators; Type: TABLE DATA; Schema: public; Owner: p12_user
--

INSERT INTO public.collaborators VALUES (1, 'AMartinez', '$2b$12$yXmmb1wgHFgbR/yV3E7v8.sHZI8Pd5TB9MxGGKVsWrgJYqayWoSu6', 2, 'Alice', 'Martinez', 'alice.martin@example.com', '0601020304');
INSERT INTO public.collaborators VALUES (9, 'CDelorme', '$2b$12$w.zeGw5aTU0sLoB2/R.9ouUg5bpwsn4pgAXpWpqWnMqTfP.8Ebp4G', 1, 'Camille', 'Delorme', 'camille.delorme@example.com', '0601020304');
INSERT INTO public.collaborators VALUES (10, 'BRenard', '$2b$12$iCHlxqqVSwH.Rq.Nblu4u.TS7CGuZ2s1W.UstX/BCIb/LQBYETXvi', 3, 'Benjamin', 'Renard', 'benjamin.renard@example.com', '0601020304');
INSERT INTO public.collaborators VALUES (32, 'KDurand', '$2b$12$NEx32KoEdwTyS1hV6c8PXOhN1TfMK3jkLBd/zjGGSFqU130P2qSLa', 3, 'Kilian', 'Durand', 'kilian.durand@example.com', '0606060606');
INSERT INTO public.collaborators VALUES (33, 'CBrunel', '$2b$12$qgbU5QlWHGSbiIyccZMyYuHRYtqvNOeAtGuU.IMYA9QY8oUrgeHCG', 1, 'Christelle', 'Brunel', 'christelle.brunel@example.com', '0606060606');
INSERT INTO public.collaborators VALUES (43, 'IIvanov', '$2b$12$FNGKRXyxov6wzK9vrdQIveCyVoWkfGofxMchdINEaLv1raQhF.o0y', 2, 'Igor', 'Ivanov', 'igor.ivanov@example.com', '0706070607');
INSERT INTO public.collaborators VALUES (49, 'ALefebvre', '$2b$12$lu/M/Yz9kAUnhcgfkPTx1O7JaprLRKcGbjGVTJeiVtvwBWtbX.3xq', 2, 'Arthur', 'Lefebvre', 'arthur.lefebvfre@example.com', '0203020302');


--
-- TOC entry 3364 (class 0 OID 24613)
-- Dependencies: 216
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: p12_user
--

INSERT INTO public.customers VALUES (2, 'GreenTech Solutions', '2025-10-17', '2025-10-19', 9, 'Sophie', 'Martin', 'test.test@test.com', '0678901234');
INSERT INTO public.customers VALUES (12, 'LuminaWorks', '2025-10-27', '2025-10-27', 9, 'Éléa', 'Duval', 'elea.duval@exemple.com', '0783456789');
INSERT INTO public.customers VALUES (11, 'Pixel & Plume', '2025-10-24', '2025-10-27', 9, 'Loan', 'Kermadec', 'loan.kermadec@example.com', '0606050506');
INSERT INTO public.customers VALUES (10, 'Orchidée Digitale', '2025-10-24', '2025-10-27', 9, 'Sirine', 'Ouldane', 'sirine.ouldane@exemple.com', '0765432110');
INSERT INTO public.customers VALUES (3, 'Altosphère', '2025-10-19', '2025-10-27', 9, 'Timaël', 'Gonzalès', 'timael.gonzales@exemple.com', '0698745432');
INSERT INTO public.customers VALUES (4, 'Velvet Code', '2025-10-19', '2025-10-27', 9, 'Isis', 'Moreau', 'isis.moreau@exemple.com', '0611223344');
INSERT INTO public.customers VALUES (5, 'NovaWeb Studio', '2025-10-19', '2025-10-27', 9, 'Naël', 'Carminati', 'nael.carminati@exemple.com', '0692135700');
INSERT INTO public.customers VALUES (1, 'Durand Consulting', '2025-10-17', '2025-10-28', 33, 'Claire', 'Durand', 'claire.durand@example.com', '0612345677');


--
-- TOC entry 3360 (class 0 OID 24586)
-- Dependencies: 212
-- Data for Name: statuses; Type: TABLE DATA; Schema: public; Owner: p12_user
--

INSERT INTO public.statuses VALUES (1, 'Signed');
INSERT INTO public.statuses VALUES (2, 'Pending');
INSERT INTO public.statuses VALUES (3, 'Unsigned');


--
-- TOC entry 3366 (class 0 OID 24629)
-- Dependencies: 218
-- Data for Name: contracts; Type: TABLE DATA; Schema: public; Owner: p12_user
--

INSERT INTO public.contracts VALUES (3, 608, 250, '2025-10-21', 2, 1);
INSERT INTO public.contracts VALUES (2, 1500, 1000, '2025-10-21', 1, 1);
INSERT INTO public.contracts VALUES (4, 800, 600, '2025-10-24', 3, 2);
INSERT INTO public.contracts VALUES (6, 500, 500, '2025-10-27', 5, 1);
INSERT INTO public.contracts VALUES (8, 900, 900, '2025-10-28', 10, 1);
INSERT INTO public.contracts VALUES (7, 2000, 2000, '2025-10-27', 1, 2);
INSERT INTO public.contracts VALUES (5, 600, 0, '2025-10-24', 5, 3);


--
-- TOC entry 3368 (class 0 OID 24646)
-- Dependencies: 220
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: p12_user
--

INSERT INTO public.events VALUES (4, 'Fréjus', 12, 'Top vendeurs', '2025-11-28', '2025-11-28', 3, 32);
INSERT INTO public.events VALUES (2, 'Nice', 50, 'Team building', '2025-12-03', '2025-12-03', 3, 32);
INSERT INTO public.events VALUES (5, 'Grasse', 200, 'Rassemblement de parfumeurs', '2025-12-15', '2025-12-16', 3, 32);
INSERT INTO public.events VALUES (3, 'Cannes', 75, 'Festival de Cannes', '2026-05-20', '2026-05-20', 2, 10);
INSERT INTO public.events VALUES (1, 'Antibes', 150, 'Conférence sur le climat', '2025-11-18', '2025-11-19', 2, 10);
INSERT INTO public.events VALUES (8, 'Vallauris', 50, 'Yatch festivities', '2025-12-28', '2025-12-28', 4, NULL);
INSERT INTO public.events VALUES (9, 'Menton', 400, 'Lemon festival', '2026-02-16', '2026-02-18', 3, NULL);
INSERT INTO public.events VALUES (6, 'Nice', 150, 'Aviation', '2025-12-16', '2025-12-16', 4, 32);
INSERT INTO public.events VALUES (7, 'Eze', 200, 'nietzsche contest', '2025-12-20', '2025-12-20', 5, 32);
INSERT INTO public.events VALUES (10, 'Gourdon', 15, 'Team buildin hiking', '2025-10-30', '2025-10-30', 6, NULL);
INSERT INTO public.events VALUES (11, 'Caussol', 15, 'Team building hiking', '2025-10-31', '2025-10-31', 8, NULL);


--
-- TOC entry 3374 (class 0 OID 0)
-- Dependencies: 213
-- Name: collaborators_id_seq; Type: SEQUENCE SET; Schema: public; Owner: p12_user
--

SELECT pg_catalog.setval('public.collaborators_id_seq', 52, true);


--
-- TOC entry 3375 (class 0 OID 0)
-- Dependencies: 217
-- Name: contracts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: p12_user
--

SELECT pg_catalog.setval('public.contracts_id_seq', 8, true);


--
-- TOC entry 3376 (class 0 OID 0)
-- Dependencies: 215
-- Name: customers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: p12_user
--

SELECT pg_catalog.setval('public.customers_id_seq', 12, true);


--
-- TOC entry 3377 (class 0 OID 0)
-- Dependencies: 209
-- Name: departments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: p12_user
--

SELECT pg_catalog.setval('public.departments_id_seq', 3, true);


--
-- TOC entry 3378 (class 0 OID 0)
-- Dependencies: 219
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: p12_user
--

SELECT pg_catalog.setval('public.events_id_seq', 11, true);


--
-- TOC entry 3379 (class 0 OID 0)
-- Dependencies: 211
-- Name: statuses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: p12_user
--

SELECT pg_catalog.setval('public.statuses_id_seq', 3, true);


-- Completed on 2025-10-31 13:49:24

--
-- PostgreSQL database dump complete
--

\unrestrict 6PSsmRken6ghKLNAlu4bALehcmMyPa4AweFwFSpkvysEqRhYbH8PVszvEJyc1Qv

