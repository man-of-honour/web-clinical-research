ALTER TABLE trials
UPDATE trials SET med = 'Аспирин' WHERE trial_name = 'Trial_Aspirin';
UPDATE trials SET med = 'Ибупрофен' WHERE trial_name = 'Trial_Ibuprofen';
UPDATE trials SET med = 'Метформин' WHERE trial_name = 'Trial_Metformin';
UPDATE trials SET med = 'Аторвастатин' WHERE trial_name = 'Trial_Atorvastatin';
UPDATE trials SET med = 'Лизиноприл' WHERE trial_name = 'Trial_Lisinopril';
UPDATE trials SET med = 'Амоксициллин' WHERE trial_name = 'Trial_Amoxicillin';
ADD COLUMN med VARCHAR(100);