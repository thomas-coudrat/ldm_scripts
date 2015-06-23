NAME
	sccomp - prediction of side chains on a fix backbone

SYNOPSIS
	sccomp [-b] [-c] [-C] [-f] [-g] [-h] [-i] [-l] [-mu] [-mr] [-o] [-p] [-r] 
	       [-R] [-s] [-t] [-tc] [-tf] [-w] coordinates_file
	
DESCRIPTION
	The program gets a PDB format file and puts side chains on the backbone 
	according to the input options. The scoring function is based on contact 
	surface areas and chemical properties with additional terms for internal energy 
	and excluded volume.
	Two methods might be used for simultaneous positioning of several side chains: 
	self-consistence and stochastic method. The first method is faster with an average 
	run time of less than a minute (860Mhz, 512MB, Pentium III), for protein of 200
	residues, while the second takes about 12 minutes, but gives somewhat better results. 
	The program makes use of the BBDEP library of Dunbrack (Dunbrack and Cohen, 
	Protein Science, 1997, 6:1661-1681).
	The command line options permit modeling of only several side chains while the 
	other are held fixed in the input conformations. 
	Mutations of any number of residues on the sequence are also allowed.
	The input structure should be in PDB format with obligatory ".pdb" suffix. 
	The order of the atoms for each residue should be according to the PDB order. 
	The coordinates of at least 4 backbone atoms (N,CA,C,O) should be given for each 
	residue, otherwise the residue will not be modeled.
	
OPTIONS
     	Command line options are described below. Every flag should appear with a value 
	following the '=' sign. For example -f=2.
	
	-b	CB
		[-b=1] Use CB coordinates if available in the input file. [-b=0] Construct CB
		according to the charmm22 standard parameters. Default [-b=0].
		
	-c	Chains
		[-c=X] Model the side chains of the residues of chain X. See also [-C] option.
		Default [-c=' ']. Using the default, all side chains of all chains will be 
		modeled. 
	
	-C	Contacting Chains
		[-C=0] Will not include the residues of other chains except the one specified 
		with the [-c] flag in the energy calculations. [-C=1] Will include any residue 
		of any chain in the calculation. In any case the residues of other chains 
		will be treated as fixed and will appear in the output file. Default [-C=1].
		 	
	-f	Fine search
		[-f=1] In case of clashing of a rotamer local search is performed for 
		dihedral angles values close to the library values. [-f=0] Check only 
		library values.  Default [-f=1].
		
	-g	loG file.
		[-g=1] create LOG file PDB_FILE_NAME.LOG which documents parameters of the 
		run and list side chains having higher probability to be wrongly 
		positioned according to self-consistency or high-energy criteria.
		[-g=0] No LOG file is created. Default [-g=0].
		
	-h	Help
		[-h] Show the help page and return from the program.
		
	-i	Iterations
		[-i=N] Perform N passes over all the flexible side chains in 
		the iterative self-consistence search. Default [-i=6].
		
	-l	Ligands
		[-l=0] Ligands are not considered for energy calculation and only presented
		in the output file. [-l=1] Ligand atoms are considered for the energy 
		calculation. The prediction is usually better but the position of the 
		ligands should be known in advance which is usually not the case in realistic
		situations.
		
	-mu	Modeling subset of side chains and MUtations
		[-mu=AAAXXXC,XXXC-XXXC] Model subset of side chains and mutations, but only
		for the exact residues which were specified. All the other side chains 
		including such with direct contact with the specified residue are held fixed. 
		AAA is residue name to be modeled in the XXX position. C is optional chain 
		identifier. In addition a range of residues might be given. All the residues
		in the range will be modeled. In this format no mutations can be specified.
		Note that no spaces are allowed inside the term.
		Examples:
		
		sccomp -mu=52 1ifc.pdb : will model residue 52 in the file 1ifc.pdb.
		No name (AAA) is given so the original amino acid type in this position 
		(in this case serine) will be modeled (no mutation). 
		
		sccomp -mu=THR52 1ifc.pdb : will mutate the serine in position 52 into 
		threonine
		
		sccomp -mu=THR52,53-54 1ifc.pdb : will mutate the serine in position 52 into
		threonine and in addition model the side chains of residues 53 (serine) and 
		54 (aspargine).
		 
		sccomp -mu=THR52,53-55,78 1ifc.pdb  : will mutate the serine in position 52 
		into threonine and in addition model the side chains of residues 53 (serine),
		54 (aspargine),55 (phenylalanine) and 78 (leucine).
		
		sccomp -mu=17E,20E-30E 3apr.pdb : will model the side chains in positions 17
		and 20 to 30 in chain E of the file 3apr.pdb.
		
		sccomp -mu=PHE17E,20E-30E 3apr.pdb : will mutate the side chains in 
		position 17 chain E (now tyrosine) into phenylalanine and will model all 
		side chains in positions 20 to 30 in chain E of the file 3apr.pdb.
		
		XXX is according to the numbers of residues in ATOM part of the PDB file.
		AAA and C should be in capitals. The entire expression must be with no spaces.
		
	-mr	Modeling Region for subset of the side chains/mutations
		[-mu=AAAXXXC,XXXC-XXXC] Model subset of side chains/mutations and also all 
		side chains in the region of the specified residues. The syntax is exactly 
		as for [-mu]. Examples:
		
		sccomp -mu=52 1ifc.pdb : will model residue 52 in the file 1ifc.pdb and all
		its contacting side chains. No residue name is given so the original 
		amino acid type in this position (in this case serine) will be modeled 
		(no mutation).

		sccomp -mu=THR52,53-54 1ifc.pdb : will mutate the serine in position 52 into 
		threonine and in addition model the side chains of residues 53 (serine) and 54 
		(aspargine). All side chains which might potentially contact threonine on 
		position 52, serine in position 53 or aspargine in position 54 will also be
		modelled.
			
	-o	Output PDB file
		[-o=0] The output PDB file will include both the input coordinates and the 
		model as different chains	
		[-o=1] The output PDB file will include only the model. Default [-o=1]. 
		
	-p	Probability of rotamers
		[-p=x] This will determine the lowest probability of rotamer in the 
		rotamer library to be examined in the modeling procedure. x is a real number 
		between [0..1]. The higher the probability the faster the execution time, 
		but the prediction accuracy might go worse. Default [-p=0.003]. 
	
	-r	Results
		[-r=1] Will create results file that summarize the prediction obtained by the 
		program in terms of percent of correct chi angles and RMSD of side chain heavy 
		atoms. [-r=0] Will not create such file. Default [-r=0].
		
	-R	Probe Radius
		[-R=x] Will determine the radius of the probe ("solvent") atom for the 
		calculation of contact surfaces and accessible surface. Empirical results show
		that 0.7A gave the best prediction results. Value of 1.4
		will create solvent accessible surface as commonly accepted in the literature. 
		The smaller this number, the faster the execution time. Default [-R=0.7].
		
	-s	Searching procedure
		[-s=0] Will perform self-consistence iterative procedure with 
		average running time of less than 1 minute (on 850MhZ, 512MB PentiumIII). 
		[-s=1] Will make stochastic approach with an average running time of 
		about 12 minutes. The second approach gives somewhat better prediction.
		Default [-s=0].
		
	-t	Evaluation Threshold
		[-t=40] Means that all modeled dihedral angles within 40 degrees from the 
		experimental values are considered correct.  Default [-t=40].
		
	-tc	Template Chain identifier
		[-tc=c] Specify the polypeptide chain c which serves as a template from
		the file specified in the -tf flag. Default [-tc=' '].
		
	-tf	Template File 
		[-tf=x.pdb] This use the specified file (x.pdb) as a template to construct
		side chain for the input structure. Global alignment with dynamic programming
		(Myers and Miller, CABIOS, 1989, 4:11-17) is done between the model and the
		template. The conformation of all residues which are conserved are copied 
		from the template and treated as fixed. The other residues are than modeled 
		by the program. The alignment is kept in the file "alignment"
		Examples: 
		
		sccomp -tf=xxx.pdb yyy.pdb : will align the amino acid sequences of xxx.pdb 
		and yyy.pdb. All the side chains conformations of the conserved residues are 
		copied from the template xxx.pdbonto the being built model. The rest of the 
		side chains are then modeled.
		
		sccomp -tf=xxx.pdb -tc=C yyy.pdb : will align the amino acid sequences of 
		xxx.pdb and chain C of yyy.pdb. All the side chains conformations of the 
		conserved residues are copied from the template xxx.pdbonto the being built 
		model. The rest of the side chains are then modeled.
	
	-w	Water (HOH)
		[-w=0] The water molecules from the input file will not be read, will not
		contribute to the energy calculation and will not appear in the output file. 
		[-w=1] The water molecules from the input will not contribute 
		to the energy calculation, but will appear in the output file. [-w=2] The water 
		molecules will contribute to the energy calculation (experimental position) 
		and will appear in the output file. Default [-w=0].

AUTHOR
	Written by Eran Eyal, Department of Plant Sciences, Weizmann Insitute of Science, 
	Oct 2002	

CONTACT
	Questions, remarks and report bugs to eran.eyal@weizmann.ac.il

