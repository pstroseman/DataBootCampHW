
# coding: utf-8

# #### PyPoll
# 
# * In this challenge, you are tasked with helping a small, rural town modernize its vote-counting process. (Up until now, Uncle Cleetus had been trustfully tallying them one-by-one, but unfortunately, his concentration isn't what it used to be.)
# 
# * You will be give a set of poll data called [election_data.csv](PyPoll/Resources/election_data.csv). The dataset is composed of three columns: `Voter ID`, `County`, and `Candidate`. Your task is to create a Python script that analyzes the votes and calculates each of the following:
# 
#   * The total number of votes cast
# 
#   * A complete list of candidates who received votes
# 
#   * The percentage of votes each candidate won
# 
#   * The total number of votes each candidate won
# 
#   * The winner of the election based on popular vote.
# 
# * As an example, your analysis should look similar to the one below:
# 
#   ```text
#   Election Results
#   -------------------------
#   Total Votes: 3521001
#   -------------------------
#   Khan: 63.000% (2218231)
#   Correy: 20.000% (704200)
#   Li: 14.000% (492940)
#   O'Tooley: 3.000% (105630)
#   -------------------------
#   Winner: Khan
#   -------------------------
#   ```
# 
# * In addition, your final script should both print the analysis to the terminal and export a text file with the results.


# Incorporated the csv module
import csv
import os

# Files to load and output (Remember to change these)
file_to_load = os.path.join("election_data.csv")
file_to_output = os.path.join("election_analysis.txt")

# Total Vote Counter
total_votes = 0

# Candidate Options and Vote Counters
candidate_options = []
candidate_votes = {}

# Winning Candidate and Winning Count Tracker
winning_candidate = ""
winning_count = 0

# Read the csv and convert it into a list of dictionaries
with open(file_to_load) as election_data:
    reader = csv.reader(election_data)

    # Read the header
    header = next(reader)

    # For each row...
    for row in reader:

        # Run the loader animation
        print(". ", end=""),

        # Add to the total vote count
        total_votes = total_votes + 1

        # Extract the candidate name from each row
        candidate_name = row[2]

        # If the candidate does not match any existing candidate...
        # (In a way, our loop is "discovering" candidates as it goes)
        if candidate_name not in candidate_options:

            # Add it to the list of candidates in the running
            candidate_options.append(candidate_name)

            # And begin tracking that candidate's voter count
            candidate_votes[candidate_name] = 0

        # Then add a vote to that candidate's count
        candidate_votes[candidate_name] = candidate_votes[candidate_name] + 1

# Print the results and export the data to our text file
with open(file_to_output, "w") as txt_file:

    # Print the final vote count (to terminal)
    election_results = (
        f"\n\nElection Results\n"
        f"-------------------------\n"
        f"Total Votes: {total_votes}\n"
        f"-------------------------\n")
    print(election_results, end="")

    # Save the final vote count to the text file
    txt_file.write(election_results)

    # Determine the winner by looping through the counts
    for candidate in candidate_votes:

        # Retrieve vote count and percentage
        votes = candidate_votes.get(candidate)
        vote_percentage = float(votes) / float(total_votes) * 100

        # Determine winning vote count and candidate
        if (votes > winning_count):
            winning_count = votes
            winning_candidate = candidate

        # Print each candidate's voter count and percentage (to terminal)
        voter_output = f"{candidate}: {vote_percentage:.3f}% ({votes})\n"
        print(voter_output, end="")

        # Save each candidate's voter count and percentage to text file
        txt_file.write(voter_output)

    # Print the winning candidate (to terminal)
    winning_candidate_summary = (
        f"-------------------------\n"
        f"Winner: {winning_candidate}\n"
        f"-------------------------\n")
    print(winning_candidate_summary)

    # Save the winning candidate's name to the text file
    txt_file.write(winning_candidate_summary)

