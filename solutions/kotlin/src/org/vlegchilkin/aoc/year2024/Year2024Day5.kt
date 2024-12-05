package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*


/**
 * 2024/5: Print Queue
 */
class Year2024Day5(input: String) : Solution {
  private val rules: List<Pair<Int, Int>>
  private val reports: List<List<Int>>

  init {
    val (rulesData, reportsData) = input.toList("\n\n") { it.split("\n") }
    this.reports = reportsData.map { it.toIntList() }
    this.rules = rulesData.map { it.toIntList().toPair() }
  }

  override fun partAB(): Pair<Int, Int> {
    val graph: Graph<Int> = this.rules
      .groupBy({ it.first }, { it.second })
      .mapValues { (_, v) -> v.toSet() }

    fun isCorrect(report: List<Int>): Boolean {
      report.fold(mutableSetOf<Int>()) { prefix, current ->
        graph[current]?.let { postfixes ->
          if (postfixes.any { it in prefix }) return false
        }
        prefix.apply {
          add(current)
        }
      }
      return true
    }

    fun score(report: List<Int>) = report[report.size / 2]

    val (correct, incorrect) = this.reports.partition { isCorrect(it) }

    val partA = correct.sumOf { score(it) }
    val partB = incorrect.map { graph.topologicalSort(it) }.sumOf { score(it) }

    return partA to partB
  }

  companion object : Test(2024, 5, { Year2024Day5(it) })
}
