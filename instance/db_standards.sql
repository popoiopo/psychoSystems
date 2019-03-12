INSERT INTO yes_no(name)
VALUES
	("Yes"),
    ("No");

INSERT INTO titles(name)
VALUES
	("Mr."),
    ("Ms."),
    ("Mss."),
    ("Dr."),
    ("Prof."),
    ("MSc.");

INSERT INTO accepteds(name, description)
VALUES
	("Yes","Accepted without question"),
    ("No", "Refused without question"),
    ("Pending", "Some questions remain that need to be asked");

INSERT INTO affiliations(name, description)
VALUES
	("Experience Expert", "Laymen who has experience with depression"),
    ("Social Worker", "Someone who works with people who are depressed"),
    ("Researcher", "Someone who is a researcher of depression");

INSERT INTO temp_aspects(name)
VALUES
    ("Miliseconds"),
	("Seconds"),
    ("Minutes"),
    ("Hours"),
    ("Days"),
    ("Weeks"),
    ("Months"),
    ("Years"),
    ("Lifetime");

INSERT INTO temp_imps(name)
VALUES
	("Onset"),
    ("Maintenance"),
    ("Relapse"),
    ("Onset & Maintenance"),
    ("Onset & Relapse"),
    ("Maintenance & Relapse"),
    ("All");


INSERT INTO operators(name)
VALUES
	("No operator needed"),
    ("if"),
    ("or"),
    ("xor"),
    ("and");

INSERT INTO node_types(name, code, size, color)
VALUES
    ("stock", '\uf187', 50, '#57169a'),
    ("cloud", '\uf0c2', 50, '#aa00ff'),
    ("unknown", '\uf128', 50, '#aa00ff');    

INSERT INTO nodes(expert_id, threshold, factor)
VALUES
    (2, 1, "Stress"),
    (2, 1, "Negative_attributional_style"),
    (2, 1, "Neuroticism"),
    (2, 1, "Dysfunctional_attitudes"),
    (2, 1, "Dysfunctional_believes"),
    (2, 1, "Residual_depressive_symptoms"),
    (2, 1, "Negative_emotionality"),
    (2, 1, "Response_style"),
    (2, 1, "Age"),
    (2, 1, "Sex"),
    (2, 1, "Baseline_depression_symptoms"),
    (2, 1, "Latent_dysfunctional_cognition"),
    (2, 1, "Immunology_markers"),
    (2, 1, "Cortisol"),
    (2, 1, "C_reactive_protein"),
    (2, 1, "Genetic_disposition");


INSERT INTO edges(expert_id, operator_id, factor_A, factor_B, value)
VALUES
    (2, 1, 1, 2, 1),
    (2, 1, 1, 3, 1),
    (2, 1, 1, 4, 1),
    (2, 1, 1, 5, 1),
    (2, 1, 7, 3, 1),
    (2, 1, 10, 11, 1);
