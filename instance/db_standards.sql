INSERT INTO yes_no(name)
VALUES
	("Yes"),
    ("No");

INSERT INTO con_strengths(name)
VALUES
    ("Very Negative"),
    ("Negative"),
    ("Neutral"),
    ("Positive"),
    ("Very Positive");
INSERT INTO sensitivities(name)
VALUES
    ("Not Sensitive"),
    ("Low Sensitive"),
    ("Medium Sensitive"),
    ("Highly Sensitive");

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
    ("Researcher", "Someone who is a researcher of depression"),
    ("Policy", "Someone who is working with depression on a policy level");

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

INSERT INTO spat_aspects(name)
VALUES
    ("Biology"),
    ("Psychological"),
    ("Interpersonal"),
    ("Community"),
    ("Societal"),
    ("Economic"),
    ("Global");

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

INSERT INTO nodes(expert_id, factor, spat_aspect_id, temp_aspect_id, sensitivity_id)
VALUES
    (2, "Stress",1,2,1),
    (2, "Negative_attributional_style",2,8,1),
    (2, "Neuroticism",2,7,1),
    (2, "Dysfunctional_attitudes",2,8,1),
    (2, "Dysfunctional_believes",2,8,1),
    (2, "Residual_depressive_symptoms",2,7,1),
    (2, "Negative_emotionality",2,9,1),
    (2, "Response_style",2,8,1),
    (2, "Age",1,9,1),
    (2, "Sex",1,9,1),
    (2, "Baseline_depression_symptoms",1,9,1),
    (2, "Latent_dysfunctional_cognition",3,8,1),
    (2, "Immunology_markers",1,4,1),
    (2, "Cortisol",1,3,1),
    (2, "C_reactive_protein",1,2,1),
    (2, "Genetic_disposition",1,9,1);


INSERT INTO edges(expert_id, operator_id, factor_A, factor_B, con_strength_id)
VALUES
    (2, 1, 1, 2, 1),
    (2, 1, 1, 3, 2),
    (2, 1, 1, 4, 3),
    (2, 1, 1, 5, 4),
    (2, 1, 7, 3, 5),
    (2, 1, 10, 11, 1);

INSERT INTO pageTexts(name, pageID, htmlName)
VALUES
    ("Depression research", "bannertitle", "index"),
    ("A complexity approach broaden our understanding", "subtitle", "index"),
    ("<h1>Creating a causal mapping of depression</h1>
        <p>Depression is a major contributor to the overall global burden of disease (WHO). Globally, more than 300 million people suffer from depression. Psychological and pharmacological treatments are effective treatments but only for half of treated patients. Further, relapse rates in depression after remission are unacceptably high. Despite a large body of research literature, effect sizes for treatment efficacy have not increased over at least four decades. Evidence for leading theories that explain the onset and maintenance of depression is fragmented (Siegle et al., 2018). Whereas, depression is seen as a disorder that is caused by interplay of mental-, biological, stress related- and societal factors that can change over time characterized by large individual differences. One of the main research challenges is to understand the causal interplay between these factors. An integrated systemic approach is the step needed to generate insights needed for the development of innovative more effective treatments. 
  For this research we aim to create and validate a causal loop model of major depression using complexity modelling, in order to identify new targets for treatment. To create this causal loop model, we conducted an extensive meta-analysis that examined the evidence for leading models for depression  (> 140.000 articles, Bockting et al., in prep.) and now we will interview leading experts.</p>", "firstText", "index"),
    ("<h1>Thank you!</h1>", "secondText", "index"),

    ("Gathering factors", "bannertitle", "fase1"),
    ("On a spatio-temporal axis", "subtitle", "fase1"),
    ("<h1>Introduction text to the table</h1>
        <p>Welcome to the first fase of our information gathering</p>", "firstText", "fase1"),
    ("<h1>Thank you for your cooperation</h1>", "secondText", "fase1"),

    ("Creating the Network", "bannertitle", "fase2"),
    ("Collaborating to create a CLD", "subtitle", "fase2"),
    ("<h1>Introduction to the CLD software</h1>
        <p>Welcome to the second fase of our information gathering. Here we tend to create the relations between causal factors of our research topic!</p>", "firstText", "fase2"),
    ("<h2>Here! Look at a simulation that we're not going to use!</h2>", "secondText", "fase2"),
    ("<h1>Thank you for your cooperation</h1>", "thirdText", "fase2");