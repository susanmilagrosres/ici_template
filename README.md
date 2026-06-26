# Selective Identity Labeling in Headlines of the New York Times (2020-2026)

## Project Description

This research project aims to identify whether minorities' identificatory labels such as "Latino", "Black" or "Indigenous" are overrepresented in the news. Other authors have proved this correct, and have suggested the analysis of large-scale news to further corroborate their results (Schulte et al, 2025). Bridging this research gap, we focus on analizying news headlines in crime-related articles of the New York Times (NYT) in the period of January 2020 to May 2026. We choose the NYT because it is seen as a neutral source (Usher, 2020) and we wonder whether such source keeps a neutral position by not over-mentioning minorities' labels. 

The media has the power of constructing and shaping our ideas of what is crime and who commits it (Kort-Butler & Habecker, 2018), these images are not just alleatory information but are ways through which the status quo is reinforced: further negative stereotypezation of minorities groups (Bonilla-Silva, 2013). Thus, the importance of this is research is on one side, to further contribute to the media literacy of the reader and empowering us by identifying these patterns; and on the other side, to raise awareness and stop stereotypezation that might influence negatively criminal justice policies. 

To analyze the NYT headlines, we first filtered all the headlines of the NYT and left only those related to crime. After that, we used LLM to identify the different associations. Further explanations of the process will be given in the sections below. 


## Getting Started

[Provide instructions on how to get started with your project, including any necessary software or data. Include installation instructions and any prerequisites or dependencies that are required.]

## File Structure

The file of the project consists of data from New York Times news outlet ranging from the start of 2020 to May 2026. The data for this research was gathered from the ProQuest database, we accessed this database through the National Chengchi University library. To ensure our dataset accurately captured the necessary crime and justice contexts, the raw data files were first filtered and categorized through keywords. The first category, Legal and Judicial, includes terms such as trials, law, enforcement, criminal sentences, indictments, court hearings and proceedings, convictions, and search warrants. The Criminal Activity category contains criminal investigations, terrorism, sex crimes, general investigations, arrests, conspiracy, mass murders, rape, and assassination attempts. Additionally, we gathered news under Public Safety and Conflict, using keywords like national security, violence, riots, shootings, rebellions, and war. Finally, the Social and Police Issues category targets socio-legal topics, including abortion, police, racism, police brutality, and assaults.

Following the initial collection, these raw data files were carefully combined and cleaned to create a unified dataset suitable to our modeling. This file contains several crucial variables that drive our methodology. The "titles" variable stores the headline of each news article, which serves as the primary text for examining identity marking and semantic frames. To manage and organize the entries, we included a unique "storeid" along with the specific "entry date" and "publication date." The extracted publication "year" allows us to effectively track temporal trends and annual shifts in media framing. Furthermore, the "subject" and "subject terms" variables help categorize the content and verify the specific crime context of each article, while the "author" variable identifies the journalist responsible for the piece. Ultimately, this streamlined file organization ensures a logical progression from raw keyword extraction to the refined data required to evaluate selective identity marking.

## Analysis
<img width="1256" height="432" alt="Screenshot 2026-06-24 223119" src="https://github.com/user-attachments/assets/9204537f-bcac-4020-a46c-6d4d38d2ec22" />

Figure 1 shows the results of the semantic frame extraction analysis, which examined how identity labels were used in crime-related New York Times articles between 2020 and 2026. The analysis focused on whether the minority and non-minority groups were explicitly identified in crime reporting and how often these labels appeared.

The findings reveal a noticeable difference in how identities were represented. As shown in Figure 1(a), minority groups were mentioned much more frequently than non-minority groups in crime-related articles. Black individuals were the most frequently labeled group with 2,099 mentions, followed by refugees with 423 mentions and Jewish individuals with 326 mentions. In comparison, White individuals were mentioned 813 times and Christians only 75 times. This suggests that minority identities were more likely to be highlighted in crime coverage.

Figure 1(b) shows a similar pattern when comparing crime and non-crime contexts. Minority identities appeared in 14.3% of crime-related articles, while non-minority identities appeared in only 3.9%. Even in non-crime articles, minority groups were labeled more often than non-minority groups. This indicates that minority identities were generally more visible in news reporting, especially when crime was involved.

Figure 1(c) further shows that identity labeling became more common as crime severity increased. The percentage of articles that included minority identity labels rose from around 12% in low-severity crimes to almost 20% in high-severity crimes. In contrast, non-minority labeling remained relatively low across all crime categories. This suggests that minority identities were more likely to be emphasized in reports about more serious crimes.

<img width="1253" height="832" alt="Screenshot 2026-06-24 223050" src="https://github.com/user-attachments/assets/908dca38-432d-4cfd-b7ba-75e95d979140" />

Figure 2 presents the temporal analysis of identity labeling in crime-related New York Times headlines between 2020 and 2026. The analysis examined how often minority and non-minority identities were mentioned over time and whether major social and political events influenced these patterns.

Figure 2(a) shows that minority identity labeling was highest in 2020, when 23.0% of crime-related headlines included a minority label. After 2020, the rate gradually declined, reaching 8.5% in 2026. Although the frequency decreased over time, minority labeling remained consistently higher than non-minority labeling throughout the entire period. Non-minority labeling stayed relatively low, ranging between 1.2% and 6.1%.

The monthly trends shown in Figure 2(b) provide a closer look at these changes. Minority labeling increased sharply during 2020 and reached its highest levels around major social and political events. One important event was the death of George Floyd in May 2020, which sparked widespread discussions about race, discrimination, and policing in the United States. Following this peak, minority labeling gradually declined but remained consistently higher than non-minority labeling.

In 2021, additional major events, including the January 6 Capitol Riot and the Atlanta spa shootings, coincided with noticeable fluctuations in identity labeling. Although these incidents were not directly associated with minority groups, the public discussions that followed often focused on issues of race, discrimination, extremism, and social inequality. As a result, minority identities continued to receive significant attention in news coverage. In contrast, non-minority labeling showed only modest fluctuations and remained relatively stable throughout the study period. This suggests that the representation of minority identities in crime-related headlines was more responsive to broader social and political developments than the representation of non-minority identities.

Figure 2(c) shows the composition of minority labels across different years. Black identities made up the largest share of minority labeling throughout the period, although their proportion decreased over time. Other groups, including Asian, refugee, Muslim, Jewish, Latino, and Indigenous identities, continued to appear but at lower levels. This indicates that the overall decline in minority labeling was mainly driven by a reduction in references to Black identities, while other minority groups maintained a smaller but consistent presence.

Figure 2(d) highlights the gap between minority and non-minority labeling. The difference was largest in 2020 at 17.0 percentage points and gradually narrowed over time. However, the gap never disappeared and remained 5.4 percentage points in 2026. This shows that minority identities continued to be labeled more frequently than non-minority identities, even as overall labeling rates declined.

<img width="1260" height="827" alt="Screenshot 2026-06-24 223152" src="https://github.com/user-attachments/assets/ca556c57-ec8e-44b8-a959-d5a3597d393c" />

Figure 3 presents the statistical modelling results used to test the hypothesis that minority identities are more explicitly labeled in crime-related New York Times content than non-minority identities. We applies several statistical method to examine whether crime context significantly influenced the likelihood of identity labeling and whether this pattern remained consistent over time.

Figure 3(a) shows the odds ratios from the logistic regression models. The results shows that crime context increased the likelihood of identity labeling for both minority and non-minority groups. However, the effect was stronger for minority identities, with an odds ratio of 1.30 compared to 1.07 for non-minority identities. Crime severity also had a positive association with identity labeling, while the negative year trend suggests that identity labeling gradually declined over time. Despite this decline, minority identities continued to show stronger associations with crime-related reporting than non-minority identities.

Figure 3(b) presents the results of the proportion test comparing identity labeling in crime and non-crime contexts. Minority identities appeared in 14.3% of crime-related articles, compared with 7.3% in non-crime articles. In contrast, non-minority identities appeared in only 3.9% of crime-related articles and 2.7% of non-crime articles. The test result was highly significant (Z = 23.76, p < 0.001), indicating that the relationship between crime reporting and minority identity labeling was unlikely to be due to chance.

Figure 3(c) further examines the relationship between identity groups and crime severity. Across low, medium, and high-severity crimes, minority identities were labeled much more frequently than non-minority identities. Non-minority labeling remained consistently low across all crime categories, while a large proportion of articles did not include any identity label. The significant chi-square result (χ² = 219.2, p < 0.001) suggests a strong association between identity group representation and crime severity.

Figure 3(d) shows how the relationship between crime context and identity labeling changed over time. Minority identities consistently recorded higher odds ratios than non-minority identities throughout the study period. The strongest effect appeared in 2020, when minority identity labeling was around three times more likely to occur in crime-related content. Although the strength of the relationship decreased in later years, minority identities remained more strongly associated with crime reporting than non-minority identities from 2020 to 2026.

## Results

Overall, our findings show that minority groups were consistently more likely to be explicitly identified than non-minority groups in crime-related New York Times headlines between 2020 and 2026. Minority identities were labeled more frequently, appeared more often in serious crime coverage, and remained more visible in crime reporting even as overall labeling rates declined after 2020. Although the gap between minority and non-minority labeling narrowed over time, statistical testing further confirmed that crime-related content was still significantly associated with minority identity labeling. These results suggest that while the intensity of identity labeling decreased over time, disparities in the representation of minority and non-minority groups remained persistent throughout the study period.

The media is more than a reflection of social phenomena; it also shapes public perceptions and attitudes toward different social groups. When minority groups are disproportionately represented in crime-related news coverage, it may strengthen the association between minority groups and crime, reinforcing stereotypes and increasing the risks of discrimination. In the long run, this kind of narrative may indirectly influence public attitude towards the minority groups, the policy making, judicial decision-making or implicit bias among law enforcement officials, potentially undermining social justice. Therefore, maintaining media neutrality and ensuring fair and balanced media representation remain important challenges. Our findings suggest that media representations may contribute to the unequal visibility of different social groups in crime reporting. They also highlight the importance of developing editorial practices that promote fair and balanced reporting while avoiding unnecessary emphasis on racial or ethnic identities. Taken together, these findings suggest that identity labeling remains an important characteristic of crime reporting and provides a basis for examining its broader implications for media representation and public perception. 

This study focuses exclusively on crime-related headlines published in the New York Times between 2020 and 2026. However, our research only indicates the correlation between major social and political events and the minority identity labeling in crime newspaper headlines, our analysis cannot establish a causal relationship and the extent of their influence between single events and the media framing. Future research should include multiple media outlets across diverse political orientations to examine how ideological stances moduleate identity labeling. Future research would benefit from extending the longitudinal scope to capture broader societal shifts, while full-text semantic analysis to better understand the broader mechanisms behind identity labeling and its social consequences.





## Contributors

[List the contributors to your project and describe their roles and responsibilities.]

Tiffany Rachel.S - 112ZU1028 In charge of final Analysis, progamming, partial data collection, data processing and cleaning. 
Erinna Tania - 112ZU1006 In charge of finding the data source, partial data collection, initial data processing and cleaning, results analysis, and poster making.
Susan M. Dávalos V. - 112ZU1041 In charge of setting the problematic + The research behind the issue + Collecting part of the data from PreQuest. 
Pin Hsuan Lin, Anita - 111ZU1003


## Acknowledgments

We acknowledge the work of our former team mate 魏彤芸 who also contributed in the data collection and distribution of the initial work. Moreover, we are in gratitute with our institution, National Chengchi University, for providing students with access to ProQuest. 

## References

Bonilla-Silva, E. (2013). Racism without Racists: Color-Blind Racism and the Persistence of Racial Inequality in America. Rowman & Littlefield Publishers, Chapter 2. 

Kort-Butler, L. A. and Habecker, P. (2018). Framing and Cultivating the Story of Crime: The Effects of Media Use, Victimization, and Social Networks on Attitudes About Crime. Criminal Justice Review 43:2, pp. 3. https://doi.org/10.1177/0734016817710696  

Schulte, N. et al. (2025). The Minority Dilemma in Communication: Why Minority Labels are Overrepresented in News Coverage. Social Psychological and Personality Science. https://doi.org/10.1177/19485506251393406

Usher, N. (2020). The New York Times in Trump’s America: A Failure for Liberals, A Champion for Liberalism. Political Communication, 37(4), 573–581. https://doi.org/10.1080/10584609.2020.1777686

[List any references or resources that you used during your project, including data sources, analytical methods, and tools.]
