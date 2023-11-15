package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.Solution

class Year2020Day6(input: String) : Solution {
  private val groups = input.trim().split("\n\n").map { it.split("\n") }


  override fun partA(): Int {
    return groups.sumOf { it.map { s -> s.toSet() }.reduce { acc, c -> acc + c }.size }
  }

  override fun partB(): Int {
    return groups.sumOf { it.map { s -> s.toSet() }.reduce { acc, c -> acc intersect c }.size }
  }

  companion object : Test(2020, 6, { Year2020Day6(it) })
}