package main

import (
	"encoding/json"
	"fmt"
	"os"
	"reflect"
	"runtime"
	"strings"

	ast "elouan-lerissel.fr/astar"
)

type outputJSON struct {
	MazePath string  `json:"mazePath"`
	Start    []int   `json:"start"`
	End      []int   `json:"end"`
	Path     [][]int `json:"path"`
}

func getMazeName(mazePath string) string {
	return strings.Split(strings.Split(mazePath, "/")[len(strings.Split(mazePath, "/"))-1], ".")[0]
}

func GetFunctionName(i interface{}) string {
	return runtime.FuncForPC(reflect.ValueOf(i).Pointer()).Name()
}

func WriteOutput(mazePath string, heuristic func(ast.Pos, ast.Pos) int, start ast.Pos, end ast.Pos, path []ast.Pos) error {
	//Get filename
	mazeName := getMazeName(mazePath)
	//Coonvert data to primitive type
	st := []int{start.X, start.Y}
	en := []int{end.X, end.Y}
	var pathArr [][]int
	for _, p := range path {
		pathArr = append(pathArr, []int{p.X, p.Y})
	}
	//Create output struct
	out := outputJSON{mazePath, st, en, pathArr}
	//Convert to JSON
	outJSON, err := json.MarshalIndent(out, "", "    ")
	if err != nil {
		return err
	}
	//Create a folder for output
	//Check if folder exists
	if _, err := os.Stat("out"); os.IsNotExist(err) {
		err = os.Mkdir("out", 0777)
		if err != nil {
			return err
		}
	}
	if _, err := os.Stat(mazeName); os.IsNotExist(err) {
		err = os.Mkdir("out/"+mazeName, 0777)
		if err != nil {
			return err
		}
	}
	if err != nil {
		return err
	}
	// Write file to output.json
	heuristicName := GetFunctionName(heuristic)
	filename := fmt.Sprintf("paths_%s_%d-%d_%d-%d.json", heuristicName, st[0], st[1], en[0], en[1])
	if _, err := os.Stat("out/" + mazeName + "/" + filename); err == nil {
		err = os.Remove("out/" + mazeName + "/" + filename)
		if err != nil {
			return err
		}
	}
	file, err := os.Create("out/" + mazeName + "/" + filename)
	if err != nil {
		return err
	}
	//Write JSON to file
	_, err = file.Write(outJSON)
	if err != nil {
		return err
	}
	defer file.Close()
	return nil
}
