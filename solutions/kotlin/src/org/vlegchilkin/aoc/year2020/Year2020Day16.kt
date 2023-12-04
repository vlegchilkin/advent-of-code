package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.Solution
import org.vlegchilkin.aoc.toList

class Year2020Day16(input: String) : Solution {
  private val fields: List<Pair<String, List<IntRange>>>
  private val your: List<Int>
  private val nearby: List<List<Int>>

  init {
    val (fieldsData, yourData, nearbyData) = input.toList("\n\n") { it }

    val rulesPattern = """^([\w\s]+): (\d+)-(\d+) or (\d+)-(\d+)$""".toRegex()
    fields = fieldsData.split("\n")
      .map { rulesPattern.matchEntire(it)!!.groupValues }
      .map { it[1] to it.drop(2).map { s -> s.toInt() }.chunked(2).map { r -> r[0]..r[1] } }

    your = yourData.split("\n")[1].let { it.split(",").map { s -> s.toInt() } }
    nearby = nearbyData.split("\n").drop(1).map { it.split(",").map { s -> s.toInt() } }
  }

  private fun invalidFieldsSum(ticket: List<Int>): Int? {
    fun isValid(num: Int): Boolean {
      return fields.map { it.second }.flatten().any { num in it }
    }
    return ticket.filter { !isValid(it) }.let { if (it.isEmpty()) null else it.sum() }
  }

  override fun partA(): Int {
    return nearby.sumOf { invalidFieldsSum(it) ?: 0 }
  }

  override fun partB(): Long {
    val tickets = nearby.filter { invalidFieldsSum(it) == null } + listOf(your)

    val possibleFields = fields.indices.associateWith { fields.indices.toMutableSet() }.toMutableMap()
    tickets.forEach { numbers ->
      possibleFields.forEach { (place, fields) ->
        fields.removeIf { !this.fields[it].second.any { range -> numbers[place] in range } }
      }
    }

    val placeToField = mutableMapOf<Int, Int>()
    while (possibleFields.isNotEmpty()) {
      possibleFields.filter { (_, v) -> v.size == 1 }.forEach { (place, fields) ->
        val field = fields.first()
        placeToField[place] = field
        possibleFields.remove(place)
        possibleFields.values.forEach { it.remove(field) }
      }
    }

    return placeToField.mapValues { (_, v) -> fields[v].first }
      .filter { (_, v) -> v.startsWith("departure") }
      .keys
      .map { your[it] }
      .fold(1L) { a, b -> a * b }
  }


  companion object : Test(2020, 16, { Year2020Day16(it) })
}