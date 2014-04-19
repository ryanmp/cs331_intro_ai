LATEX_FILENAME	= report

default: latex runall

latex: $(LATEX_FILENAME).tex
	pdflatex $(LATEX_FILENAME).tex
	rm *.out *.log *.aux

runall:
	python hw1.py testStart1.txt testGoal1.txt bfs out1_bfs.txt
	python hw1.py testStart2.txt testGoal2.txt bfs out2_bfs.txt
	python hw1.py testStart3.txt testGoal3.txt bfs out3_bfs.txt

	python hw1.py testStart1.txt testGoal1.txt dfs out1_dfs.txt
	python hw1.py testStart2.txt testGoal2.txt dfs out2_dfs.txt
	python hw1.py testStart3.txt testGoal3.txt dfs out3_dfs.txt

	python hw1.py testStart1.txt testGoal1.txt iddfs out1_iddfs.txt
	python hw1.py testStart2.txt testGoal2.txt iddfs out2_iddfs.txt
	python hw1.py testStart3.txt testGoal3.txt iddfs out3_iddfs.txt

	python hw1.py testStart1.txt testGoal1.txt astar out1_astar.txt
	python hw1.py testStart2.txt testGoal2.txt astar out2_astar.txt
	python hw1.py testStart3.txt testGoal3.txt astar out3_astar.txt

clean:
	rm out*.txt


