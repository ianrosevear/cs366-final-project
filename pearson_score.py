from scipy.stats import pearsonr
import numpy as np

#old: ianscores = [2,2,0,2,2,0,2,3,1,2,1,1,2,2,1,3,3,1,2,2,1,2,1,0,1,2,2,0]
#old: celiascores = [3,2,0,2,3,0,2,3,1,1,1,2,3,2,2,0,4,0,3,1,0,2,1,0,0,0,1,0]

ianscores = [0,0,0,0,1,1,0,0,0,0,0,2,0,2,0,1,4,0,1,0,0,2,0,2,3,0,1,0,0,0]
celiascores = [0,1,0,0,2,2,0,0,0,0,1,2,2,2,0,0,1,0,1,0,0,1,0,2,3,0,0,1,0,0]

score = pearsonr(ianscores, celiascores)

print("Pearson correlation coefficient:", round(score[0], 4))
imean = np.mean(ianscores)
cmean = np.mean(celiascores)
tmean = (imean + cmean) / 2

print("Ian's mean score:", round(imean, 4),
      "\nCelia's mean score:", round(cmean, 4),
      "\nCombined mean score:", round(tmean, 4))
