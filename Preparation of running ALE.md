## 3. Make a tree
### Run tree_of_mags under python environment and in dataset file
Input directory: /bio/data/Lianchun/faa

Output directory: /bio/data/Lianchun/faa

     tree_of_mags --dir /bio/data/Lianchun/short_faa_filenames
Save the document called "concatenated_alignment"
#### 3.1 Use FastTree to make a tree
Input path and file: /bio/data/Lianchun/dataset/alignments/concatenated_alignment

Output file: fasttree_file
      
     fasttree /bio/data/Lianchun/dataset/alignments/concatenated_alignment > fasttree_file
#### 3.2 Use raxml to make a tree. 
     raxmlHPC-PTHREADS -s alignments/concatenated_alignment -n raxml-tree -m PROTGAMMALG -f a -p 13 -x 123 -# 100 -T 16

Or run RAxML on [CIPRES Science Gateway](https://www.phylo.org/portal2/login!input.action): 

Here is the command for the CIPRES running RAxMl Blackbox: 
    
     raxmlHPC-HYBRID-AVX -T 4 -s infile -N autoMRE -n result -f a -p 12345 -x 12345 -m PROTCATJTT
#### 3.3 Use iq_tree to make a tree. 
I run iq_tree on a webpage, which is called [IQTREE Web Server:](http://iqtree.cibiv.univie.ac.at/)
Here is the command for how the IQTREE web server works

      nohup iqtree2 –s /bio/data/Lianchun/tree_of_mags_run_Tuesday/alignments/concatenated_alignment &
Then upload the *fasttree_file*, *RAxML_bestTree.result* and *concatenated_alignment.treefile* to [ITOL](https://itol.embl.de/upload.cgi), which is an online tool to make a tree
***
## 4. Run checkm2 to check the Completeness and Contamination of genomes.
Extension format: fna

The path of input directory: /bio/data/Lianchun/fna

The path of output directory: /bio/data/Lianchun/checkm2

Activate checkm2 environment

     source /bio/bin/checkm2/bin/activate
Export libraries path

     export LD_LIBRARY_PATH=/bio/bin/lib:/bio/bin/python38/pkg/python38/usr/lib
Run checkm2

    checkm2 predict -t 30 -x fna --input /bio/data/Lianchun/fna --output-directory /bio/data/Lianchun/checkm2
It will take a while.

Open *quality_report_checkm2.tsv*. Screened out genomes with **completeness < 90** and **contamination > 5-10**.
***
## 5. Run metaerg to annotation
Follow [Dr. Strous's metaerg](https://github.com/kinestetika/MetaErg).
Activate a virtual environment for metaerg
    
     python -m virtualenv metaerg-env
     source metaerg-env/bin/activate

Should run this command in output directory. Since metaerg will spend more than **40 min for 1 genome**, we should use **nohup** to put the program to the background.

Put all the progress to the terminal

     nohup <your-command> &
Run metaerg command:

Input directory: /bio/data/Lianchun/fna

Database directory: /bio/databases/metaerg

     nohup metaerg --contig_file /bio/data/Lianchun/fna --database_dir /bio/databases/metaerg --file_extension .fna --output_dir /bio/data/Lianchun/metaerg_run_Wednesday & 
Check the running status

     htop
     less log.txt
     less nohup.out
Check whose commands

     pstree -aup

Kill a process. PID can be found by the "top" command.

     kill <PID>

***
## 6. Use a loop command to run clustalo omega (multiply sequence alignment)

    for file in /bio/data/Lianchun/orthologues_run_Friday/*.faa; do clustalo -i "$file" -o /bio/data/Lianchun/mp_sq_al/"$(basename "$file" .faa)".aln ; done
***
## 7. Creates ultrafast bootstrap tree distributions

The original iqtree2 command:
      
    iqtree2 -s /bio/data/Lianchun/mp_sq_al/*.aln -m MFP -madd LG+C20,LG+C60 -B 10000 -wbtl

Combine loop and nohup command to run iqtree2

    nohup sh -c 'for file in /bio/data/Lianchun/mp_sq_al/*.aln; do iqtree2 -s "$file" -m MFP -madd LG+C20,LG+C60 -B 10000 -wbtl ; done' &

Save all the **.ufboot** files.

Check the permission of those .ufboot files.
Make sure that everyone can write.
If not, use the command below to change the permission:

    for file in /bio/data/Lianchun/ALEobserve/*.ufboot; do chmod 666 "$file" ; done
Or try **chmod 777** as a substitution way.
***