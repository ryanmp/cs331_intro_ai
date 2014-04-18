LATEX_FILENAME	= report

default: latex run

latex: $(LATEX_FILENAME).tex
	pdflatex $(LATEX_FILENAME).tex
	rm *.out *.log *.aux

run: out.txt
	python hw1.py testStart2.txt testGoal2.txt bfs out.txt