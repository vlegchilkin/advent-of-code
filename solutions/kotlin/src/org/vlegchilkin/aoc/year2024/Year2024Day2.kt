package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*
import kotlin.math.absoluteValue


/**
 * 2024/2: Red-Nosed Reports
 */
class Year2024Day2(input: String) : Solution {
  private val reports = input.toList { it.toIntList() }

  private fun isSafe(report: Sequence<Int>): Boolean {
    val dec = report.zipWithNext { a, b -> a > b }.all { it }
    val inc = report.zipWithNext { a, b -> a < b }.all { it }
    val dif = report.zipWithNext { a, b -> (a - b).absoluteValue }.all { it in 1..3 }
    return (dec or inc) and dif
  }

  override fun partA(): Int {
    return reports.count { isSafe(it.asSequence()) }
  }

  override fun partB(): Any {
    return reports.count { report ->
      IntRange(0, report.size).any { badLevelIndex ->
        val filteredReport = report.asSequence().filterIndexed { index, _ -> index != badLevelIndex }
        isSafe(filteredReport)
      }
    }
  }

  companion object : Test(2024, 2, { Year2024Day2(it) })
}
