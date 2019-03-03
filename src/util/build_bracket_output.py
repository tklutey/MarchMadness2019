from bracketeer import build_bracket

base_url = '/Users/kluteytk/development/projects/MarchMadness2019/'
def build_bracket_output():
    b = build_bracket(outputPath=base_url + 'output.png',
                      teamsPath=base_url + 'data/raw/Teams.csv',
                      seedsPath=base_url + 'data/raw/NCAATourneySeeds.csv',
                      submissionPath=base_url + 'data/processed/2019Predictions.csv',
                      slotsPath=base_url + 'data/raw/NCAATourneySlots.csv',
                      year=2019
                      )

if __name__ == '__main__':
    build_bracket_output()
