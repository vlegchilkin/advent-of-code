package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*
import kotlin.math.absoluteValue


/**
 * 2024/1: Historian Hysteria
 */
class Year2024Day1(input: String) : Solution {
  private val lines = input.toList { it.toIntList().toPair() }

  override fun partAB(): Pair<Int, Int> {
    val first = lines.map { it.first }
    val second = lines.map { it.second }
    val partA = first.sorted().zip(second.sorted()).sumOf { (f, s) -> (f - s).absoluteValue }

    val secondCounter = second.groupingBy { it }.eachCount()
    val partB = first.sumOf { it * secondCounter.getOrElse(it) { 0 } }
    return partA to partB
  }

  companion object : Test(2024, 1, { Year2024Day1(it) })
}
