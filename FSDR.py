import pandas as pd

try:
    from IPython.display import Markdown
except ImportError:
    Markdown = lambda x: x

def FSDR(df, main_col, other_col, rel_thresh=30, abs_thresh=None, return_text=True, markdown=True,
         value_suffix="", comparison_text_larger='larger', comparison_text_smaller='smaller',
         value_format_str='', intro_text=""):
    # Copy df so any changes we make aren't propagated back to the calling function
    df = df.copy()
    
    # Calculate difference, absolute difference and percentage difference (relative to main_col)
    diff = df[main_col] - df[other_col]
    abs_diff = diff.abs()
    perc_diff = (abs_diff / df[main_col]) * 100
    
    # Calculate rows that are significantly different because the percentage difference is over the relative threshold
    if rel_thresh is not None:
        sig_diff_by_perc = set(perc_diff[perc_diff > rel_thresh].index)
    else:
        sig_diff_by_perc = set()
    
    # Calculate rows that are significantly different because the absolute difference is over the absolute threshold
    if abs_thresh is not None:
        sig_diff_by_abs = set(abs_diff[abs_diff > abs_thresh].index)
    else:
        sig_diff_by_abs = set()
    
    # Union these two to get *all* significantly different rows
    sig_diff_rows = sig_diff_by_perc.union(sig_diff_by_abs)
    
    # If we don't want the text (just the row indexes) then return now
    if not return_text:
        return list(sig_diff_rows)
    
    # Get the subset of the data frame that contains the significantly different rows
    # and sort descending by the values in main_col - so that we get the biggest ones at the top
    just_sig_rows = df.loc[list(sig_diff_rows)]
    just_sig_rows = just_sig_rows.sort_values(main_col, ascending=False)
    
    output_text = intro_text
    
    # Iterate through the rows and generate the text according to the template
    for item, row in just_sig_rows.iterrows():
        main_val = row[main_col]
        other_val = row[other_col]
        
        if main_val > other_val:
            comparison_text = comparison_text_larger
        else:
            comparison_text = comparison_text_smaller
        
        if markdown:
            italics = "_"
            bold = "**"
        else:
            italics = ""
            bold = ""

        row = (f' - {bold}{item}{bold} is significantly {italics}{comparison_text}{italics} for {main_col} '
               f'({main_val:{value_format_str}}{value_suffix} for {main_col} '
               f'compared to {other_val:{value_format_str}}{value_suffix} for {other_col})\n')
        
        output_text += row
    
    if markdown:
        return Markdown(output_text)
    else:
        return output_text