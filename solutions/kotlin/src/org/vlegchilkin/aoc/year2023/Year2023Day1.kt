package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.Solution
import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.trimSplitMap

/**
 * 2023/1: Trebuchet?!
 */
class Year2023Day1(input: String) : Solution {
  private val lines = input.trimSplitMap { it }
  override fun partA(): Any {
    return lines.sumOf { line ->
      val digits = line.filter { it.isDigit() }.map { it - '0' }
      digits.first() * 10 + digits.last()
    }
  }

  override fun partB(): Any {
    val nums = arrayOf("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")

    return lines.sumOf { line ->
      val digits = line.mapIndexedNotNull { index, c ->
        when(c) {
          in '0'..'9' -> c - '0'
          else -> {
            val num = nums.indexOfFirst { s -> line.startsWith(s, index) } + 1
            if (num > 0) num else null
          }
        }
      }
      digits.first() * 10 + digits.last()
    }
  }

  companion object : Test(2023, 1, { Year2023Day1(it) })
}