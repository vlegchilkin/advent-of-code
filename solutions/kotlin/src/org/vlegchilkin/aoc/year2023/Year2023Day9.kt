package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*


/**
 * 2023/9: Mirage Maintenance
 */
class Year2023Day9(input: String) : Solution {
  private val lines = input.toList { it.toLongList() }

  override fun partA(): Long {
    fun extRight(line: List<Long>): Long {
      var current = line
      var right = 0L
      while (!current.all { it == 0L }) {
        right += current.last()
        current = current.windowed(2) { it[1] - it[0] }
      }
      return right
    }
    return lines.sumOf { extRight(it) }
  }

  override fun partB(): Long {
    fun extLeft(line: List<Long>): Long {
      var current = line
      val left = mutableListOf<Long>()
      while (!current.all { it == 0L }) {
        left += current.first()
        current = current.windowed(2) { it[1] - it[0] }
      }
      return left.reversed().fold(0L) { acc, c -> c - acc}
    }
    return lines.sumOf { extLeft(it) }
  }

  companion object : Test(2023, 9, { Year2023Day9(it) })
}
