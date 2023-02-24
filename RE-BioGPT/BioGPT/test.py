import torch
from src.transformer_lm_prompt import TransformerLanguageModelPrompt
m = TransformerLanguageModelPrompt.from_pretrained(
        "checkpoints/RE-BC5CDR-BioGPT", 
        "checkpoint_avg.pt", 
        "data/BC5CDR/relis-bin",
        tokenizer='moses', 
        bpe='fastbpe', 
        bpe_codes="data/bpecodes",
        max_len_b=1024,
        beam=1)

src_text="Acute hepatitis associated with clopidogrel: a case report and review of the literature. Drug-induced hepatotoxicity is a common cause of acute hepatitis, and the recognition of the responsible drug may be difficult. We describe a case of clopidogrel-related acute hepatitis. The diagnosis is strongly suggested by an accurate medical history and liver biopsy. Reports about cases of hepatotoxicity due to clopidogrel are increasing in the last few years, after the increased use of this drug. In conclusion, we believe that physicians should carefully consider the risk of drug-induced hepatic injury when clopidogrel is prescribed." # input text, e.g., a PubMed abstract
src_text2="An unexpected diagnosis in a renal-transplant patient with proteinuria treated with everolimus: AL amyloidosis. Proteinuria is an expected complication in transplant patients treated with mammalian target of rapamycin inhibitors (mTOR-i). However, clinical suspicion should always be supported by histological evidence in order to investigate potential alternate diagnoses such as acute or chronic rejection, interstitial fibrosis and tubular atrophy, or recurrent or de novo glomerulopathy. In this case we report the unexpected diagnosis of amyloidosis in a renal-transplant patient with pre-transplant monoclonal gammapathy of undetermined significance who developed proteinuria after conversion from tacrolimus to everolimus."
src_text="Bortezomib and dexamethasone as salvage therapy in patients with relapsed/refractory multiple myeloma: analysis of long-term clinical outcomes. Bortezomib (bort)-dexamethasone (dex) is an effective therapy for relapsed/refractory (R/R) multiple myeloma (MM). This retrospective study investigated the combination of bort (1.3 mg/m(2) on days 1, 4, 8, and 11 every 3 weeks) and dex (20 mg on the day of and the day after bort) as salvage treatment in 85 patients with R/R MM after prior autologous stem cell transplantation or conventional chemotherapy. The median number of prior lines of therapy was 2. Eighty-seven percent of the patients had received immunomodulatory drugs included in some line of therapy before bort-dex. The median number of bort-dex cycles was 6, up to a maximum of 12 cycles. On an intention-to-treat basis, 55 % of the patients achieved at least partial response, including 19 % CR and 35 % achieved at least very good partial response. Median durations of response, time to next therapy and treatment-free interval were 8, 11.2, and 5.1 months, respectively. The most relevant adverse event was peripheral neuropathy, which occurred in 78 % of the patients (grade II, 38 %; grade III, 21 %) and led to treatment discontinuation in 6 %. With a median follow up of 22 months, median time to progression, progression-free survival (PFS) and overall survival (OS) were 8.9, 8.7, and 22 months, respectively. Prolonged PFS and OS were observed in patients achieving CR and receiving bort-dex a single line of prior therapy. Bort-dex was an effective salvage treatment for MM patients, particularly for those in first relapse."

NER_annt_NL=" In this abstract, everolimus is a chemical, proteinuria is a disease, amyloidosis is a disease."

src_tokens = m.encode(src_text2+NER_annt_NL)

generate = m.generate([src_tokens], beam=1)[0]
output = m.decode(generate[0]["tokens"])
print(output)
