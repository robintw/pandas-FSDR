import pandas as pd

try:
    from IPython.display import Markdown
except ImportError:
    Markdown = lambda x: x

def FSDR(df, main_col, other_col, rel_thresh=30, abs_thresh=None, return_text=True, markdown=True,
         value_suffix="", comparison_text_larger='larger', comparison_text_smaller='smaller'):
    diff = df[main_col] - df[other_col]
    abs_diff = diff.abs()
    perc_diff = (abs_diff / df[main_col]) * 100
    
    if rel_thresh is not None:
        sig_diff_by_perc = set(perc_diff[perc_diff > rel_thresh].index)
    else:
        sig_diff_by_perc = set()
        
    if abs_thresh is not None:
        sig_diff_by_abs = set(abs_diff[abs_diff > abs_thresh].index)
    else:
        sig_diff_by_abs = set()
    
    sig_diff_rows = sig_diff_by_perc.union(sig_diff_by_abs)
    
    if not return_text:
        return list(sig_diff_rows)
    
    output_text = f"When comparing {main_col} with {other_col}:\n\n"
    
    for item in sig_diff_rows:
        row = df.loc[item]
        main_val = row[main_col]
        other_val = row[other_col]
        
        if main_val > other_val:
            comparison_text = comparison_text_larger
        else:
            comparison_text = comparison_text_smaller
        
        row = f' - {item} is significantly {comparison_text} for {main_col} ({main_val}{value_suffix} for {main_col} compared to {other_val}{value_suffix} for {other_col})\n'
        
        output_text += row
    
    if markdown:
        return Markdown(output_text)
    else:
        return output_text