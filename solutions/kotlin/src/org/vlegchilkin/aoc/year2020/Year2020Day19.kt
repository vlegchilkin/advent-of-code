package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.*

class Year2020Day19(input: String) : Solution {
  private val messages: List<String>
  private val rules: Map<Int, List<List<Any>>>

  init {
    val (rulesData, messages) = input.trimSplitMap("\n\n") { it.split("\n") }
    this.messages = messages

    val pattern = """^(\d+): (.*)$""".toRegex()
    rules = rulesData.map { rd ->
      val (_, parent, children) = pattern.matchEntire(rd)!!.groupValues
      parent.toInt() to children.split('|')
        .map { r ->
          r.trim().split(' ')
            .map { if (it[0] == '"') it.drop(1).dropLast(1) else it.toInt() }
        }
    }.toMap()
  }

  private fun verify(rules: Map<Int, List<List<Any>>>): Int {
    val cache = rules.keys.associateWith { HashMap<String, Boolean>() }

    fun isValid(ruleId: Int, str: String): Boolean {
      val record = cache[ruleId]!!
      record[str]?.let { return it }

      rules[ruleId]?.forEach { creds ->
        if (creds.size == 1) {
          if (creds[0] is String) {
            return (creds[0] == str).also { record[str] = it }
          }
          if (isValid(creds[0] as Int, str)) {
            return true.also { record[str] = true }
          }
        }
        else if (creds.size == 2) {
          val (a, b) = creds.map { it as Int }
          for (i in 1..<str.length) {
            if (isValid(a, str.substring(0, i)) && isValid(b, str.substring(i))) {
              return true.also { record[str] = true }
            }
          }
        }
        else if (creds.size == 3) {
          val (a, b, c) = creds.map { it as Int }
          for (i in 2..<str.length) {
            for (j in 1..<i) {
              if (isValid(a, str.substring(0, j)) && isValid(b, str.substring(j, i)) && isValid(c, str.substring(i))) {
                return true.also { record[str] = true }
              }
            }
          }
        }
      }
      return false.also { record[str] = false }
    }

    return messages.count { isValid(0, it) }
  }

  override fun partA(): Int {
    return verify(rules)
  }

  override fun partB(): Int {
    val modified = rules.toMutableMap()
    modified[8] = modified[8]!!.toMutableList().also { it.add(listOf(42, 8)) }
    modified[11] = modified[11]!!.toMutableList().also { it.add(listOf(42, 11, 31)) }
    return verify(modified)
  }

  companion object : Test(2020, 19, { Year2020Day19(it) })
}
