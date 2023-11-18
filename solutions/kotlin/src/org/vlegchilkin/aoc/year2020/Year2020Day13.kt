package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.Solution
import java.math.BigInteger

class Year2020Day13(input: String) : Solution {
  private val timestamp: Int
  private val routes: List<Int?>

  init {
    val (_, ts, data) = """^(\d+)\n(.*)\n$""".toRegex().matchEntire(input)!!.groupValues
    timestamp = ts.toInt()
    routes = data.split(',').map { if (it == "x") null else it.toInt() }
  }

  override fun partA(): Int {
    val result = routes
      .filterNotNull()
      .map { it to it * ((timestamp + it - 1) / it) - timestamp }
      .minBy { it.second }
    return result.first * result.second
  }

  /**
   * https://en.wikipedia.org/wiki/Chinese_remainder_theorem
   * 0) r{i} = T % a{i}  (which equals to a{i}-i by the time T due to the task definition)
   * 1) m = a1 * a2 * ... * an
   * 2) n = [m/a1, m/a2, ..., m/an]
   * 3) nInverse{i} = modInverse(n{i}, a{i})
   * 4) T = sum( r{i} * n{i} * nInverse{i} ) % m
   */
  override fun partB(): Long {
    val a = routes.filterNotNull().map { it.toLong() }
    val r = routes.mapIndexedNotNull { index, x -> if (x != null) x - index else null }
    val m = a.reduce { acc, x -> acc * x }
    val n = a.map { m / it }
    val nInverse = n.mapIndexed { i, it -> BigInteger.valueOf(it).modInverse(BigInteger.valueOf(a[i])).toLong() }
    return a.indices.sumOf { r[it] * n[it] * nInverse[it] } % m
  }

  companion object : Test(2020, 13, { Year2020Day13(it) })
}