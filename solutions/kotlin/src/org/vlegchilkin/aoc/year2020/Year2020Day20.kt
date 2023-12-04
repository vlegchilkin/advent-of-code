package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.*
import kotlin.math.sqrt

class Year2020Day20(input: String) : Solution {
  private val files: Map<Int, Array<IntArray>>
  private val n: Int
  private val m: Int

  init {
    val pattern = """^Tile (\d+):$""".toRegex()
    files = input.toList("\n\n") { it.split("\n") }.associate {
      pattern.matchEntire(it[0])!!.groupValues[1].toInt() to
        it.drop(1).map { line -> line.map { c -> (c == '#').toInt() }.toIntArray() }.toTypedArray()
    }
    n = sqrt(files.size.toDouble()).toInt()
    m = files.values.first().size
  }


  private fun puzzle(): Pair<Array<IntArray>, Array<IntArray>> {
    val space = Array(n * m) { IntArray(n * m) { 0 } }
    val mapping = Array(n) { IntArray(n) { 0 } }
    val translations = files.mapValues { (_, v) -> translate(v) }
    val unusedFiles = files.keys.toMutableSet()

    fun fits(row: Int, col: Int, slide: Array<IntArray>): Boolean {
      if (row > 0 && (0..<m).any { slide[0][it] != space[(row - 1) * m + m - 1][(col * m) + it] }) {
        return false
      }
      if (col > 0 && (0..<m).any { slide[it][0] != space[(row * m) + it][(col - 1) * m + m - 1] }) {
        return false
      }
      return true
    }

    fun fill(row: Int, col: Int, slide: Array<IntArray>) {
      slide.forEachIndexed { r, line ->
        line.forEachIndexed { c, value ->
          space[row * m + r][col * m + c] = value
        }
      }
    }

    fun dfs(index: Int): Boolean {
      if (index == n * n) return true
      val (row, col) = index / n to index % n
      unusedFiles.toList().forEach { fileId ->
        translations[fileId]!!.filter { fits(row, col, it) }.forEach {
          fill(row, col, it)
          unusedFiles.remove(fileId)
          mapping[row][col] = fileId
          if (dfs(index + 1)) return true
          unusedFiles.add(fileId)
        }
      }
      return false
    }
    dfs(0)
    return mapping to space
  }

  override fun partAB(): Pair<Long, Int> {
    val (mapping, space) = puzzle()
    val partA = 1L * mapping[0][0] * mapping[0][n - 1] * mapping[n - 1][0] * mapping[n - 1][n - 1]

    var partB: Int? = null

    val mask = arrayOf(
      intArrayOf(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
      intArrayOf(1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1),
      intArrayOf(0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0),
    )

    val compact = Array(n * (m - 2)) { IntArray(n * (m - 2)) { 0 } }
    for (row in 0..<n) {
      for (col in 0..<n) {
        for (i in 0..<m - 2) {
          for (j in 0..<m - 2) {
            compact[row * (m - 2) + i][col * (m - 2) + j] = space[row * m + i + 1][col * m + j + 1]
          }
        }
      }
    }

    fun fits(area: Array<IntArray>, rowOffset: Int, colOffset: Int ): Boolean {
      return mask.filterIndexed{ r, line ->
        line.filterIndexed{ c, value -> (value == 1 && area[r+rowOffset][c+colOffset] != 1) }.any()
      }.isEmpty()
    }

    translate(compact).forEach { area ->
      var found = false
      for (rowOffset in 0..compact.size-mask.size) {
        for (colOffset in 0..compact.size-mask[0].size) {
          if (fits(area, rowOffset, colOffset)) {
            mask.forEachIndexed {r, line ->
              line.forEachIndexed { c, value ->
                area[r + rowOffset][c + colOffset] -= value
              }
            }
            found = true
          }
        }
      }
      if (found) {
        partB = area.sumOf { it.sum() }
        return@forEach
      }
    }

    return partA to partB!!
  }


  companion object : Test(2020, 20, { Year2020Day20(it) })
}