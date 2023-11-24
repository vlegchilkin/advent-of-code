package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.Solution
import org.vlegchilkin.aoc.trimSplitMap

class Year2020Day21(input: String) : Solution {
  private val foods = input.trimSplitMap() {
    val (_, ingredientsData, allergensData) = PATTERN.matchEntire(it)!!.groupValues
    ingredientsData.split(' ').toSet() to allergensData.split(", ").toSet()
  }

  override fun partAB(): Pair<Any, Any> {
    val possible = mutableMapOf<String, MutableSet<String>>()
    foods.forEach { (ingredients, allergens) ->
      allergens.forEach {
        possible.compute(it) { _, v ->
          (if (v == null) ingredients else v intersect ingredients).toMutableSet()
        }
      }
    }
    val marked = possible.values.fold(mutableSetOf<String>()) { union, values -> union.apply { addAll(values) } }
    val partA = foods.map { it.first }.sumOf { f -> f.count { it !in marked } }

    val resolved = mutableSetOf<String>()
    do {
      val single = possible.filter { (k, v) -> k !in resolved && v.size == 1 }
      resolved.addAll(single.keys)
      val ingredients = single.values.flatten().toSet()
      possible.values.filter { it.size > 1 }.forEach {
        it.removeAll(ingredients)
      }
    }
    while (single.isNotEmpty())
    val partB = possible.toSortedMap().values.flatten().joinToString(",")

    return partA to partB
  }

  companion object : Test(2020, 21, { Year2020Day21(it) }) {
    val PATTERN = """^([\w\s]+) \(contains ([\w\s,]+)\)$""".toRegex()
  }
}