package main

import (
	"image"
	"io"
	"os"

	"golang.org/x/image/bmp"
)

func ReadBitmap(path string) ([][]int, error) {
	// You can register another format here
	image.RegisterFormat("bmp", "bmp", bmp.Decode, bmp.DecodeConfig)

	file, err := os.Open(path)

	if err != nil {
		return nil, err
	}

	defer file.Close()

	pixels, err := getArray(file)

	if err != nil {
		return nil, err

	}
	return pixels, nil
}

// Get the bi-dimensional pixel array
func getArray(file io.Reader) ([][]int, error) {
	img, _, err := image.Decode(file)

	if err != nil {
		return nil, err
	}

	bounds := img.Bounds()
	width, height := bounds.Max.X, bounds.Max.Y

	var arr [][]int
	for y := 0; y < height; y++ {
		var row []int
		for x := 0; x < width; x++ {
			row = append(row, rgbToBit(img.At(x, y).RGBA()))
		}
		arr = append(arr, row)
	}

	return arr, nil
}

// img.At(x, y).RGBA() returns four uint32 values; we want a Pixel
func rgbToBit(r uint32, g uint32, b uint32, a uint32) int {
	if r > 0 {
		return 1
	}
	return 0
}
